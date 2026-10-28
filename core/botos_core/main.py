"""Discord bot entrypoint."""

from __future__ import annotations

import asyncio
import logging

import discord
from discord.ext import commands

from botos_core.config import load_settings
from botos_core.constants import DEFAULT_MAX_GUILD_COMMANDS
from botos_core.plugin_manager import PluginManager

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def build_bot(*, plugin_manager: PluginManager) -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = False
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:
        logger.info("Logged in as %s (id=%s)", bot.user, bot.user.id if bot.user else "?")
        settings = load_settings()
        if settings.sync_global_commands_on_ready:
            synced = await bot.tree.sync()
            logger.info("Synced %d global application command(s)", len(synced))
        cmd_total = plugin_manager.total_command_count() + len(
            [c for c in bot.tree.walk_commands() if c.parent is None]
        )
        if cmd_total > DEFAULT_MAX_GUILD_COMMANDS:
            logger.warning(
                "Command count %d exceeds default guild limit %d",
                cmd_total,
                DEFAULT_MAX_GUILD_COMMANDS,
            )

    @bot.tree.command(name="botos_ping", description="BotOS core connectivity check")
    async def botos_ping(interaction: discord.Interaction) -> None:
        await interaction.response.send_message("BotOS core is running.", ephemeral=True)

    return bot


async def async_main() -> int:
    settings = load_settings()
    if not settings.discord_bot_token:
        logger.error("DISCORD_BOT_TOKEN is not set. Copy .env.example to .env and configure it.")
        return 1

    plugins = PluginManager()
    try:
        plugins.discover_standard_plugins()
    except (ValueError, TypeError) as exc:
        logger.error("Failed to load plugins: %s", exc)
        return 1
    logger.info("Loaded plugin ids: %s", plugins.list_ids())

    bot = build_bot(plugin_manager=plugins)
    try:
        await bot.start(settings.discord_bot_token)
    finally:
        if not bot.is_closed():
            await bot.close()
    return 0


def main() -> None:
    try:
        code = asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Shutting down.")
        code = 0
    raise SystemExit(code)


if __name__ == "__main__":
    main()
