"""Guild plugin install/list and sync queue."""

from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from botos_api.db.models import Guild, GuildPlugin, GuildSyncRequest, Plugin


async def ensure_guild(session: AsyncSession, guild_id: str, *, name: str = "Unknown") -> Guild:
    guild = await session.get(Guild, guild_id)
    if guild is None:
        guild = Guild(id=guild_id, name=name[:100])
        session.add(guild)
        await session.flush()
    return guild


async def upsert_plugin_record(
    session: AsyncSession,
    *,
    plugin_id: str,
    manifest: dict[str, Any],
) -> Plugin:
    plugin = await session.get(Plugin, plugin_id)
    if plugin is None:
        plugin = Plugin(
            id=plugin_id,
            name=str(manifest.get("name", plugin_id))[:100],
            description=str(manifest.get("description", ""))[:500] or None,
            type=str(manifest.get("type", "blockly")),
            is_public=bool(manifest.get("is_public", False)),
            manifest=manifest,
            content={
                "entrypoint": manifest.get("entrypoint", {}),
            },
        )
        session.add(plugin)
    else:
        plugin.manifest = manifest
        plugin.content = {"entrypoint": manifest.get("entrypoint", {})}
    await session.flush()
    return plugin


async def install_guild_plugin(
    session: AsyncSession,
    *,
    guild_id: str,
    plugin_id: str,
    manifest: dict[str, Any],
    guild_name: str = "Unknown",
) -> GuildPlugin:
    await ensure_guild(session, guild_id, name=guild_name)
    await upsert_plugin_record(session, plugin_id=plugin_id, manifest=manifest)
    row = await session.scalar(
        select(GuildPlugin).where(
            GuildPlugin.guild_id == guild_id,
            GuildPlugin.plugin_id == plugin_id,
        )
    )
    if row is None:
        row = GuildPlugin(
            id=str(uuid.uuid4()),
            guild_id=guild_id,
            plugin_id=plugin_id,
            is_enabled=True,
            config={},
        )
        session.add(row)
    else:
        row.is_enabled = True
    await request_guild_sync(session, guild_id)
    await session.flush()
    return row


async def list_guild_plugins(session: AsyncSession, guild_id: str) -> list[dict[str, Any]]:
    rows = await session.scalars(select(GuildPlugin).where(GuildPlugin.guild_id == guild_id))
    result: list[dict[str, Any]] = []
    for row in rows:
        plugin = await session.get(Plugin, row.plugin_id)
        result.append(
            {
                "plugin_id": row.plugin_id,
                "is_enabled": row.is_enabled,
                "name": plugin.name if plugin else row.plugin_id,
            }
        )
    return result


async def request_guild_sync(session: AsyncSession, guild_id: str) -> None:
    existing = await session.get(GuildSyncRequest, guild_id)
    if existing is None:
        session.add(GuildSyncRequest(guild_id=guild_id))
    await session.flush()
