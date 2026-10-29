"""Discord bot entrypoint."""

from __future__ import annotations

import asyncio
import logging

import discord
from discord.ext import commands

from botos_core.command_router import PluginCommandRouter
from botos_core.config import load_settings
from botos_core.event_dispatch import dispatch_member_join
from botos_core.plugin_manager import PluginManager
from botos_core.sandbox.runner import SandboxRunner
from botos_core.sync_worker import guild_sync_worker

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def build_bot(*, plugin_manager: PluginManager, router: PluginCommandRouter) -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = False
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    sandbox = SandboxRunner()

    @bot.event
    async def on_ready() -> None:
        logger.info("Logged in as %s (id=%s)", bot.user, bot.user.id if bot.user else "?")
        settings = load_settings()
        if settings.sync_global_commands_on_ready:
            synced = await bot.tree.sync()
            logger.info("Synced %d global application command(s)", len(synced))

    @bot.tree.command(name="botos_ping", description="BotOS core connectivity check")
    async def botos_ping(interaction: discord.Interaction) -> None:
        await interaction.response.send_message("BotOS core is running.", ephemeral=True)

    @bot.listen("on_member_join")
    async def on_member_join_plugin_dispatch(member: discord.Member) -> None:
        try:
            await dispatch_member_join(str(member.guild.id), member, sandbox)
        except Exception:
            logger.exception("on_member_join plugin dispatch failed")

    bot.botos_router = router  # type: ignore[attr-defined]
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

    router = PluginCommandRouter()
    bot = build_bot(plugin_manager=plugins, router=router)
    worker_task = asyncio.create_task(guild_sync_worker(bot, router))
    try:
        await bot.start(settings.discord_bot_token)
    finally:
        worker_task.cancel()
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
