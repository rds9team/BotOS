"""Loads `.botos.json` plugins and tracks enable/disable per guild.

Implementation stub: extend `load_plugin_manifest` and `plugins_for_guild`.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
        self._plugins_root = plugins_root or Path(__file__).resolve().parents[2] / "plugins"
        self._by_id: dict[str, PluginManifest] = {}

    def discover_standard_plugins(self) -> None:
        """Scan `plugins/standard/*/*.botos.json`."""
        standard = self._plugins_root / "standard"
        if not standard.is_dir():
            logger.warning("No plugins directory at %s", standard)
            return
        for path in standard.glob("*/*.botos.json"):
            manifest = load_plugin_manifest(path)
            self._by_id[manifest.id] = manifest
            logger.info("Discovered plugin %s@%s", manifest.id, manifest.version)

    def get(self, plugin_id: str) -> PluginManifest | None:
        return self._by_id.get(plugin_id)

    def list_ids(self) -> list[str]:
        return sorted(self._by_id.keys())


def load_plugin_manifest(path: Path) -> PluginManifest:
    data = json.loads(path.read_text(encoding="utf-8"))
    plugin_id = data.get("id")
    if not plugin_id:
        msg = f"Missing 'id' in {path}"
        raise ValueError(msg)
    return PluginManifest(
        id=str(plugin_id),
        name=str(data.get("name", plugin_id)),
        version=str(data.get("version", "0.0.0")),
        raw=data,
    )
