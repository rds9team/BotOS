"""Seed standard plugins from disk into DB."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from botos_api.services.guild_plugins import upsert_plugin_record
from botos_core.plugin_manager import PluginManager


async def sync_standard_plugins_to_db(session: AsyncSession) -> list[str]:
    manager = PluginManager()
    manager.discover_standard_plugins()
    ids: list[str] = []
    for plugin_id in manager.list_ids():
        manifest = manager.get(plugin_id)
        if manifest is None:
            continue
        await upsert_plugin_record(session, plugin_id=plugin_id, manifest=manifest.raw)
        ids.append(plugin_id)
    await session.commit()
    return ids
