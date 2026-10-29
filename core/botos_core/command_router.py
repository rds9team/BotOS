"""Dispatch slash commands to sandboxed plugin handlers."""

from __future__ import annotations

import logging
from typing import Any

import discord

from botos_core.sandbox.runner import SandboxRunner
from botos_core.sandbox.wrapper import SandboxInteractionContext

logger = logging.getLogger(__name__)


class PluginCommandRouter:
    def __init__(self, sandbox: SandboxRunner | None = None) -> None:
        self._sandbox = sandbox or SandboxRunner()

    async def handle_slash_command(
        self,
        interaction: discord.Interaction,
        manifest: dict[str, Any],
        command_name: str,
    ) -> None:
        ctx = SandboxInteractionContext(interaction)
        result = await self._sandbox.run_plugin_command(manifest, command_name, ctx)
        if not result.ok:
            message = result.error or "Plugin error"
            logger.warning("Plugin command failed: %s", message)
            await ctx.reply(message, ephemeral=True)
            return
        replies = _action_list(result.value, "replies")
        for reply in replies:
            content = str(reply.get("content", ""))
            ephemeral = bool(reply.get("ephemeral", False))
            await ctx.reply(content, ephemeral=ephemeral)


def _action_list(value: Any, key: str) -> list:
    if not isinstance(value, dict):
        return []
    actions = value.get(key)
    return actions if isinstance(actions, list) else []
