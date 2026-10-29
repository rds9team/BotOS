"""Background worker processing guild sync requests from API."""

from __future__ import annotations

import asyncio
import logging

from discord.ext import commands

from botos_core.command_router import PluginCommandRouter
from botos_core.guild_state import get_enabled_plugin_manifests, pop_pending_sync_guild_ids
from botos_core.guild_sync import sync_guild_commands

logger = logging.getLogger(__name__)


async def guild_sync_worker(bot: commands.Bot, router: PluginCommandRouter) -> None:
    while not bot.is_closed():
        try:
            guild_ids = await pop_pending_sync_guild_ids()
            for guild_id in guild_ids:
                manifests = await get_enabled_plugin_manifests(guild_id)
                await sync_guild_commands(
                    bot,
                    int(guild_id),
                    manifests,
                    router=router,
                )
        except Exception as exc:
            logger.exception("Guild sync worker error: %s", exc)
        await asyncio.sleep(2)
