"""Regression tests for bug fixes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.engine import make_url

from botos_api.main import _ensure_sqlite_parent_dir, create_app
from botos_core.plugin_manager import PluginManager, load_plugin_manifest


def test_load_plugin_manifest_rejects_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.botos.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_plugin_manifest(bad)


def test_plugin_manager_skips_duplicate_ids(tmp_path: Path) -> None:
    standard = tmp_path / "standard" / "a"
    standard.mkdir(parents=True)
    manifest = {
        "id": "dup.test",
        "name": "A",
        "version": "1.0.0",
        "type": "blockly",
        "commands": [],
        "events": [],
        "permissions": [],
    }
    (standard / "one.botos.json").write_text(json.dumps(manifest), encoding="utf-8")
    second = tmp_path / "standard" / "b" / "two.botos.json"
    second.parent.mkdir(parents=True)
    second.write_text(json.dumps(manifest), encoding="utf-8")

    pm = PluginManager(plugins_root=tmp_path)
    pm.discover_standard_plugins()
    assert pm.list_ids() == ["dup.test"]


def test_guild_id_validation() -> None:
    app = create_app()
    client = TestClient(app)
    bad = client.get(
        "/api/guilds/not-a-snowflake/plugins",
        headers={"Authorization": "Bearer invalid"},
    )
    assert bad.status_code in (401, 422)


def test_ensure_sqlite_parent_dir(tmp_path: Path) -> None:
    db_file = tmp_path / "nested" / "botos.db"
    url = f"sqlite+aiosqlite:///{db_file}"
    _ensure_sqlite_parent_dir(url)
    assert db_file.parent.is_dir()
    parsed = make_url(url)
    assert parsed.database is not None


def test_health_uptime_after_lifespan() -> None:
    app = create_app()
    client = TestClient(app)
    stats = client.get("/api/stats").json()
    assert stats["uptime_seconds"] >= 0
