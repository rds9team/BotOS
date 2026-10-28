"""API-layer validation."""

from __future__ import annotations

from botos_core.constants import DEFAULT_MAX_GUILD_COMMANDS, MAX_PLUGIN_ID_LENGTH
from botos_core.validation import is_discord_snowflake, is_valid_plugin_id


def validate_guild_id_param(guild_id: str) -> str | None:
    if not is_discord_snowflake(guild_id):
        return "Invalid guild_id"
    return None


def validate_plugin_id_param(plugin_id: str) -> str | None:
    if not plugin_id or not plugin_id.strip():
        return "Invalid plugin_id"
    if len(plugin_id) > MAX_PLUGIN_ID_LENGTH:
        return "plugin_id too long"
    if ".." in plugin_id or "/" in plugin_id or "\\" in plugin_id:
        return "plugin_id contains unsafe characters"
    if not is_valid_plugin_id(plugin_id):
        return "Invalid plugin_id format"
    return None


def validate_requested_quota(
    quota: int,
    *,
    current_max: int = DEFAULT_MAX_GUILD_COMMANDS,
) -> str | None:
    if quota <= current_max:
        return "requested_quota must be greater than current max"
    if quota > 100:
        return "requested_quota exceeds hard limit"
    return None
