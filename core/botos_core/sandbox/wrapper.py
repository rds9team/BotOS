"""Safe Discord interaction wrapper for sandboxed plugin code."""

from __future__ import annotations

import discord


class SandboxInteractionContext:
    def __init__(self, interaction: discord.Interaction) -> None:
        self._interaction = interaction
        self.author = interaction.user
        self.channel = interaction.channel
        self.guild = interaction.guild

    async def reply(self, content: str, *, ephemeral: bool = False) -> None:
        done = self._interaction.response.is_done
        finished = done() if callable(done) else bool(done)
        if finished:
            await self._interaction.followup.send(content, ephemeral=ephemeral)
        else:
            await self._interaction.response.send_message(content, ephemeral=ephemeral)

    async def defer(self, *, ephemeral: bool = False) -> None:
        done = self._interaction.response.is_done
        finished = done() if callable(done) else bool(done)
        if not finished:
            await self._interaction.response.defer(ephemeral=ephemeral)

    def to_payload(self) -> dict:
        user = getattr(self._interaction, "user", None)
        channel = getattr(self._interaction, "channel", None)
        guild = getattr(self._interaction, "guild", None)
        return {
            "user": {
                "id": str(getattr(user, "id", "")),
                "name": str(getattr(user, "name", "unknown")),
            },
            "channel": {
                "id": str(getattr(channel, "id", "")),
                "name": str(getattr(channel, "name", "")),
            },
            "guild": {
                "id": str(getattr(guild, "id", "")),
                "name": str(getattr(guild, "name", "")),
            },
        }
