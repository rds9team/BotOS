"""Loads `.botos.json` plugins and tracks enable/disable per guild."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botos_core.repo_root import repo_root
from botos_core.validation import validate_plugin_manifest_data

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PluginManifest:
    id: str
    name: str
    version: str
    raw: dict[str, Any]


class PluginManager:
    """In-memory registry until API + DB wiring exists."""

    def __init__(self, plugins_root: Path | None = None) -> None:
        self._plugins_root = plugins_root or repo_root() / "plugins"
        self._by_id: dict[str, PluginManifest] = {}

    def discover_standard_plugins(self) -> None:
        """Scan `plugins/standard/*/*.botos.json`."""
        standard = self._plugins_root / "standard"
        if not standard.is_dir():
            logger.warning("No plugins directory at %s", standard)
            return
        for path in sorted(standard.glob("*/*.botos.json")):
            try:
                manifest = load_plugin_manifest(path)
            except (OSError, ValueError, TypeError) as exc:
                logger.error("Skipping plugin file %s: %s", path, exc)
                continue
            if manifest.id in self._by_id:
                logger.error(
                    "Duplicate plugin id %r: already loaded, skipping %s",
                    manifest.id,
                    path,
                )
                continue
            self._by_id[manifest.id] = manifest
            logger.info("Discovered plugin %s@%s", manifest.id, manifest.version)

    def get(self, plugin_id: str) -> PluginManifest | None:
        return self._by_id.get(plugin_id)

    def list_ids(self) -> list[str]:
        return sorted(self._by_id.keys())

    def total_command_count(self) -> int:
        from botos_core.validation import count_plugin_commands

        return sum(count_plugin_commands(m.raw) for m in self._by_id.values())


def load_plugin_manifest(path: Path) -> PluginManifest:
    try:
        raw_text = path.read_text(encoding="utf-8")
    except OSError as exc:
        msg = f"Cannot read plugin manifest {path}: {exc}"
        raise ValueError(msg) from exc
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        msg = f"Invalid JSON in plugin manifest {path}: {exc.msg}"
        raise ValueError(msg) from exc
    if not isinstance(data, dict):
        msg = f"Plugin manifest must be a JSON object: {path}"
        raise TypeError(msg)
    errors = validate_plugin_manifest_data(data)
    if errors:
        msg = f"Invalid plugin manifest {path}: {', '.join(errors)}"
        raise ValueError(msg)
    plugin_id = str(data["id"])
    name = str(data.get("name", plugin_id)).strip()
    if not name:
        msg = f"Empty plugin name in {path}"
        raise ValueError(msg)
    return PluginManifest(
        id=plugin_id,
        name=name,
        version=str(data["version"]),
        raw=data,
    )
