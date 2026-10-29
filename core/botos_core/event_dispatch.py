"""Dispatch Discord events to sandboxed plugin handlers."""

from __future__ import annotations

import logging
from typing import Any

from botos_core.guild_state import get_enabled_plugin_manifests
from botos_core.sandbox.runner import SandboxRunner

logger = logging.getLogger(__name__)


async def dispatch_member_join(
    guild_id: str,
    member: Any,
    sandbox: SandboxRunner,
) -> None:
    """Run `on_member_join` handlers of enabled plugins for this guild."""
    try:
        manifests = await get_enabled_plugin_manifests(guild_id)
    except Exception:
        logger.exception("Failed to load plugin manifests for guild %s", guild_id)
        return
    guild = getattr(member, "guild", None)
    for manifest in manifests:
        if "on_member_join" not in (manifest.get("events") or []):
            continue
        result = await sandbox.run_plugin_event(
            manifest,
            "on_member_join",
            member,
            manifest.get("plugin_config"),
        )
        if not result.ok:
            logger.warning(
                "Event plugin %s failed for guild %s: %s",
                manifest.get("id"),
                guild_id,
                result.error,
            )
            continue
        sends = _action_list(result.value, "channel_sends")
        for send in sends:
            channel_id = str(send.get("channel_id", ""))
            content = str(send.get("content", ""))
            try:
                await _send_to_guild_channel(guild, channel_id, content)
            except (ValueError, LookupError, AttributeError):
                logger.warning(
                    "Welcome channel send failed for guild %s (channel=%s)",
                    guild_id,
                    send.get("channel_id"),
                )


def _action_list(value: Any, key: str) -> list:
    if not isinstance(value, dict):
        return []
    actions = value.get(key)
    return actions if isinstance(actions, list) else []


async def _send_to_guild_channel(guild: Any, channel_id: str, content: str) -> None:
    if guild is None:
        raise ValueError("not in a guild")
    try:
        resolved = guild.get_channel_or_thread(int(channel_id))
    except (TypeError, ValueError):
        raise ValueError(f"invalid channel id: {channel_id!r}") from None
    if resolved is None:
        raise ValueError(f"channel not found: {channel_id}")
    await resolved.send(content[:2000])
