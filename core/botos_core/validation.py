"""Input validation helpers (security and Discord API constraints)."""

from __future__ import annotations

import re
from typing import Any

from botos_core.constants import (
    ALLOWED_PLUGIN_TYPES,
    MAX_COMMAND_NAME_LENGTH,
    MAX_EVENT_NAME_LENGTH,
    MAX_PLUGIN_ID_LENGTH,
    MAX_SNOWFLAKE_LENGTH,
    MIN_SNOWFLAKE_LENGTH,
)

_SNOWFLAKE_RE = re.compile(rf"^\d{{{MIN_SNOWFLAKE_LENGTH},{MAX_SNOWFLAKE_LENGTH}}}$")
_PLUGIN_ID_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9._-]*[a-zA-Z0-9])?$")
_COMMAND_NAME_RE = re.compile(r"^[-_a-z0-9]{1,32}$")
_SEMVER_LOOSE_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")
_EVENT_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,63}$")


def is_discord_snowflake(value: str) -> bool:
    return bool(_SNOWFLAKE_RE.match(value))


def is_valid_plugin_id(value: str) -> bool:
    if not value or len(value) > MAX_PLUGIN_ID_LENGTH:
        return False
    if ".." in value or "/" in value or "\\" in value:
        return False
    return bool(_PLUGIN_ID_RE.match(value))


def is_valid_slash_command_name(name: str) -> bool:
    if not name or len(name) > MAX_COMMAND_NAME_LENGTH:
        return False
    return bool(_COMMAND_NAME_RE.match(name))


def is_valid_plugin_type(plugin_type: str) -> bool:
    return plugin_type in ALLOWED_PLUGIN_TYPES


def is_valid_semver(version: str) -> bool:
    return bool(_SEMVER_LOOSE_RE.fullmatch(version))


def is_valid_event_name(name: str) -> bool:
    if len(name) > MAX_EVENT_NAME_LENGTH:
        return False
    return bool(_EVENT_NAME_RE.match(name))


def validate_plugin_manifest_data(data: dict[str, Any]) -> list[str]:
    """Return human-readable validation errors (empty list if OK)."""
    errors: list[str] = []
    plugin_id = str(data.get("id", ""))
    if not is_valid_plugin_id(plugin_id):
        errors.append("invalid plugin id")
    version = str(data.get("version", ""))
    if not is_valid_semver(version):
        errors.append("invalid semver version")
    plugin_type = str(data.get("type", "blockly"))
    if not is_valid_plugin_type(plugin_type):
        errors.append("invalid plugin type")
    commands = data.get("commands", [])
    if commands is not None and not isinstance(commands, list):
        errors.append("commands must be a list")
    elif isinstance(commands, list):
        for cmd in commands:
            if not isinstance(cmd, dict):
                errors.append("command entries must be objects")
                break
            cmd_name = str(cmd.get("name", ""))
            if not is_valid_slash_command_name(cmd_name):
                errors.append(f"invalid command name: {cmd_name!r}")
    events = data.get("events", [])
    if events is not None and not isinstance(events, list):
        errors.append("events must be a list")
    elif isinstance(events, list):
        for event in events:
            if not is_valid_event_name(str(event)):
                errors.append(f"invalid event name: {event!r}")
    permissions = data.get("permissions", [])
    if permissions is not None and not isinstance(permissions, list):
        errors.append("permissions must be a list")
    entrypoint = data.get("entrypoint")
    if entrypoint is not None and not isinstance(entrypoint, dict):
        errors.append("entrypoint must be an object")
    return errors


def count_plugin_commands(data: dict[str, Any]) -> int:
    commands = data.get("commands", [])
    if not isinstance(commands, list):
        return 0
    return len(commands)
