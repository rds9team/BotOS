"""Per-guild slash command registration (Discord guild sync)."""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

from botos_core.constants import DEFAULT_MAX_GUILD_COMMANDS

logger = logging.getLogger(__name__)


async def sync_guild_commands(
    bot: commands.Bot,
    guild_id: int,
    *,
    max_commands: int = DEFAULT_MAX_GUILD_COMMANDS,
) -> None:
    """Sync application commands for one guild after plugin changes."""
    if max_commands < 1:
        msg = "max_commands must be positive"
        raise ValueError(msg)
    guild = discord.Object(id=guild_id)
    command_count = len([cmd for cmd in bot.tree.walk_commands() if cmd.parent is None])
    if command_count > max_commands:
        msg = f"Guild {guild_id} would exceed command limit ({command_count}>{max_commands})"
        raise ValueError(msg)
    synced = await bot.tree.sync(guild=guild)
    logger.info("Synced %d guild command(s) for guild %s", len(synced), guild_id)
