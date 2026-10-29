"""Dynamic guild slash command registration."""

from __future__ import annotations

import logging
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands

from botos_core.command_router import PluginCommandRouter
from botos_core.constants import DEFAULT_MAX_GUILD_COMMANDS

logger = logging.getLogger(__name__)


async def sync_guild_commands(
    bot: commands.Bot,
    guild_id: int,
    plugin_manifests: list[dict[str, Any]],
    *,
    router: PluginCommandRouter,
    max_commands: int = DEFAULT_MAX_GUILD_COMMANDS,
) -> None:
    command_defs: list[tuple[str, str, dict[str, Any]]] = []
    for manifest in plugin_manifests:
        for cmd in manifest.get("commands") or []:
            if not isinstance(cmd, dict):
                continue
            name = str(cmd.get("name", ""))
            description = str(cmd.get("description", name))[:100]
            command_defs.append((name, description, manifest))

    if len(command_defs) > max_commands:
        msg = f"Guild {guild_id} exceeds command limit ({len(command_defs)}>{max_commands})"
        raise ValueError(msg)

    guild = discord.Object(id=guild_id)
    bot.tree.clear_commands(guild=guild)

    def make_callback(cmd_name: str, manifest: dict[str, Any]):
        async def callback(interaction: discord.Interaction) -> None:
            await router.handle_slash_command(interaction, manifest, cmd_name)

        return callback

    for name, description, manifest in command_defs:
        cmd = app_commands.Command(
            name=name,
            description=description,
            callback=make_callback(name, manifest),
        )
        bot.tree.add_command(cmd, guild=guild)

    synced = await bot.tree.sync(guild=guild)
    logger.info("Synced %d guild command(s) for guild %s", len(synced), guild_id)
