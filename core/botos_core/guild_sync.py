"""Per-guild slash command registration (Discord guild sync).

Stub: call from API after plugin install/enable. See `docs/architecture.md` §2.1.
"""

from __future__ import annotations

import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

DEFAULT_MAX_COMMANDS = 30


async def sync_guild_commands(
    bot: commands.Bot,
    guild_id: int,
    *,
    max_commands: int = DEFAULT_MAX_COMMANDS,
) -> None:
    """Sync application commands for one guild after plugin changes."""
    guild = discord.Object(id=guild_id)
    # TODO: build command list from enabled plugins; enforce max_commands
    logger.info(
        "Guild sync requested for %s (max_commands=%s); tree.sync not wired yet",
        guild_id,
        max_commands,
    )
    _ = bot, guild
