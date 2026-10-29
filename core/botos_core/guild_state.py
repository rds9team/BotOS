"""Load enabled plugin manifests for a guild from shared DB."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from botos_api.db.models import GuildPlugin, GuildSyncRequest, Plugin
from botos_api.db.session import get_engine


async def get_enabled_plugin_manifests(guild_id: str) -> list[dict[str, Any]]:
    engine = get_engine()
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        rows = await session.scalars(
            select(GuildPlugin).where(
                GuildPlugin.guild_id == guild_id,
                GuildPlugin.is_enabled.is_(True),
            )
        )
        manifests: list[dict[str, Any]] = []
        for row in rows:
            plugin = await session.get(Plugin, row.plugin_id)
            if plugin is None:
                continue
            manifest = dict(plugin.manifest or {})
            entrypoint = (plugin.content or {}).get("entrypoint")
            if entrypoint:
                manifest["entrypoint"] = entrypoint
            manifest["plugin_config"] = dict(row.config or {})
            manifests.append(manifest)
        return manifests


async def pop_pending_sync_guild_ids() -> list[str]:
    engine = get_engine()
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        rows = (await session.scalars(select(GuildSyncRequest))).all()
        guild_ids = [row.guild_id for row in rows]
        for row in rows:
            await session.delete(row)
        await session.commit()
        return guild_ids
