"""Discord bot entrypoint."""

from __future__ import annotations

import asyncio
import logging
import sys

import discord
from discord.ext import commands

from botos_core.config import load_settings
from botos_core.plugin_manager import PluginManager

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def build_bot() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = False
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready() -> None:
        logger.info("Logged in as %s (id=%s)", bot.user, bot.user.id if bot.user else "?")

    @bot.tree.command(name="botos_ping", description="BotOS core connectivity check")
    async def botos_ping(interaction: discord.Interaction) -> None:
        await interaction.response.send_message("BotOS core is running.", ephemeral=True)

    return bot


async def async_main() -> None:
    settings = load_settings()
    if not settings.discord_bot_token.strip():
        logger.error("DISCORD_BOT_TOKEN is not set. Copy .env.example to .env and configure it.")
        sys.exit(1)

    plugins = PluginManager()
    plugins.discover_standard_plugins()
    logger.info("Loaded plugin ids: %s", plugins.list_ids())

    bot = build_bot()
    await bot.start(settings.discord_bot_token)


def main() -> None:
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        logger.info("Shutting down.")


if __name__ == "__main__":
    main()
