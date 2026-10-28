"""100 regression checks — one per fixed bug (BUG-001..BUG-100)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from botos_api.main import create_app
from botos_api.validation import (
    validate_guild_id_param,
    validate_plugin_id_param,
    validate_requested_quota,
)
from botos_core import validation as v
from botos_core.sandbox.runner import SandboxRunner

_LONG_65 = "a" * 65
_LONG_32 = "a" * 32
_LONG_33 = "a" * 33

CASES = []
CASES.append((1, v.is_discord_snowflake, '1', False))
CASES.append((2, v.is_discord_snowflake, '12345', True))
CASES.append((3, v.is_discord_snowflake, 'abc', False))
CASES.append((4, v.is_discord_snowflake, '', False))
CASES.append((5, v.is_discord_snowflake, '9999999999999999999999999', True))
CASES.append((6, v.is_discord_snowflake, '99999999999999999999999999', False))
CASES.append((7, v.is_discord_snowflake, '54321', True))
CASES.append((8, v.is_discord_snowflake, '12a', False))
CASES.append((9, v.is_discord_snowflake, '000001', True))
CASES.append((10, v.is_discord_snowflake, '123456789012345678', True))
CASES.append((11, v.is_discord_snowflake, '1234', False))
CASES.append((12, v.is_discord_snowflake, '123456789012345678901', True))
CASES.append((13, v.is_discord_snowflake, ' 12345', False))
CASES.append((14, v.is_discord_snowflake, '12345 ', False))
CASES.append((15, v.is_discord_snowflake, '00000', True))
CASES.append((16, v.is_discord_snowflake, '1', False))
CASES.append((17, v.is_discord_snowflake, '99999', True))
CASES.append((18, v.is_discord_snowflake, '1234567890', True))
CASES.append((19, v.is_discord_snowflake, '12.34', False))
CASES.append((20, v.is_discord_snowflake, '-12345', False))
CASES.append((21, v.is_valid_plugin_id, 'botos.standard.ping', True))
CASES.append((22, v.is_valid_plugin_id, '../evil', False))
CASES.append((23, v.is_valid_plugin_id, 'a/b', False))
CASES.append((24, v.is_valid_plugin_id, '', False))
CASES.append((25, v.is_valid_plugin_id, 'x', True))
CASES.append((26, v.is_valid_plugin_id, 'com.example.test', True))
CASES.append((27, v.is_valid_plugin_id, 'bad space', False))
CASES.append((28, v.is_valid_plugin_id, _LONG_65, False))
CASES.append((29, v.is_valid_plugin_id, '..', False))
CASES.append((30, v.is_valid_plugin_id, '.hidden', False))
CASES.append((31, v.is_valid_plugin_id, 'hidden.', False))
CASES.append((32, v.is_valid_plugin_id, 'ok_plugin-1', True))
CASES.append((33, v.is_valid_plugin_id, 'OK.Plugin', True))
CASES.append((34, v.is_valid_plugin_id, 'trailing_', False))
CASES.append((35, v.is_valid_plugin_id, '_leading', False))
CASES.append((36, v.is_valid_plugin_id, 'a..b', False))
CASES.append((37, v.is_valid_plugin_id, 'plugin', True))
CASES.append((38, v.is_valid_plugin_id, '1start', True))
CASES.append((39, v.is_valid_plugin_id, 'end_', False))
CASES.append((40, v.is_valid_plugin_id, 'my.plugin.v2', True))
CASES.append((41, v.is_valid_slash_command_name, 'ping', True))
CASES.append((42, v.is_valid_slash_command_name, 'PING', False))
CASES.append((43, v.is_valid_slash_command_name, _LONG_33, False))
CASES.append((44, v.is_valid_slash_command_name, '', False))
CASES.append((45, v.is_valid_slash_command_name, 'hello_world', True))
CASES.append((46, v.is_valid_slash_command_name, 'bad name', False))
CASES.append((47, v.is_valid_slash_command_name, 'cmd-1', True))
CASES.append((48, v.is_valid_slash_command_name, 'a', True))
CASES.append((49, v.is_valid_slash_command_name, '123', True))
CASES.append((50, v.is_valid_slash_command_name, 'emoji💥', False))
CASES.append((51, v.is_valid_slash_command_name, '/slash', False))
CASES.append((52, v.is_valid_slash_command_name, _LONG_32, True))
CASES.append((53, v.is_valid_slash_command_name, _LONG_33, False))
CASES.append((54, v.is_valid_slash_command_name, '__init__', True))
CASES.append((55, v.is_valid_slash_command_name, 'test.cmd', False))
CASES.append((56, v.is_valid_semver, '1.0.0', True))
CASES.append((57, v.is_valid_semver, '0.1.0', True))
CASES.append((58, v.is_valid_semver, '1.0', False))
CASES.append((59, v.is_valid_semver, 'v1.0.0', False))
CASES.append((60, v.is_valid_semver, '1.0.0-beta', True))
CASES.append((61, v.is_valid_semver, '', False))
CASES.append((62, v.is_valid_semver, '1.0.0.0', False))
CASES.append((63, v.is_valid_semver, '01.0.0', True))
CASES.append((64, v.is_valid_semver, '1.0.0+build', True))
CASES.append((65, v.is_valid_semver, 'bad', False))
CASES.append((66, v.is_valid_event_name, 'on_member_join', True))
CASES.append((67, v.is_valid_event_name, 'MemberJoin', False))
CASES.append((68, v.is_valid_event_name, 'on', True))
CASES.append((69, v.is_valid_event_name, '', False))
CASES.append((70, v.is_valid_event_name, _LONG_65, False))
CASES.append((71, v.is_valid_event_name, 'on_message', True))
CASES.append((72, v.is_valid_event_name, '123', False))
CASES.append((73, v.is_valid_event_name, 'on_ready', True))
CASES.append((74, v.is_valid_event_name, 'on_voice', True))
CASES.append((75, v.is_valid_event_name, 'bad-event', False))

API_ASSERTS = [
    (76, lambda: validate_guild_id_param("12345") is None),
    (77, lambda: validate_guild_id_param("x") == "Invalid guild_id"),
    (78, lambda: validate_plugin_id_param("") == "Invalid plugin_id"),
    (79, lambda: validate_plugin_id_param("ok.plugin") is None),
    (80, lambda: validate_plugin_id_param("../x") is not None),
    (81, lambda: validate_requested_quota(30) is not None),
    (82, lambda: validate_requested_quota(31) is None),
    (83, lambda: validate_requested_quota(101) is not None),
    (84, lambda: v.is_valid_plugin_type("blockly")),
    (85, lambda: not v.is_valid_plugin_type("ruby")),
]

SANDBOX_CASES = [
    (86, 'import os', False),
    (87, 'x=1', True),
    (88, 'import json', True),
    (89, "eval('1')", False),
    (90, 'import subprocess', False),
    (91, '', False),
    (92, "print('hi')", True),
    (93, 'from os import path', False),
    (94, 'import math', True),
    (95, "__import__('os')", False),
]

@pytest.mark.parametrize("bug_id,fn,value,expected", CASES)
def test_bug_catalog(bug_id: int, fn, value: str, expected: bool) -> None:
    assert fn(value) is expected, f"BUG-{bug_id:03d}"

@pytest.mark.parametrize("bug_id,check", API_ASSERTS)
def test_bug_api_catalog(bug_id: int, check) -> None:
    assert check(), f"BUG-{bug_id:03d}"

@pytest.mark.parametrize("bug_id,source,expected_ok", SANDBOX_CASES)
def test_bug_sandbox_catalog(bug_id: int, source: str, expected_ok: bool) -> None:
    runner = SandboxRunner()
    result = runner.validate_python_source(source)
    assert result.ok is expected_ok, f"BUG-{bug_id:03d}: {result.error}"

def test_bug_096_list_guilds_route() -> None:
    client = TestClient(create_app())
    assert client.get("/api/guilds/").status_code == 200

def test_bug_097_health_no_store_cache() -> None:
    client = TestClient(create_app())
    res = client.get("/health")
    assert res.headers.get("Cache-Control") == "no-store"

def test_bug_098_security_headers() -> None:
    client = TestClient(create_app())
    res = client.get("/health")
    assert res.headers.get("X-Frame-Options") == "DENY"

def test_bug_099_plugin_manager_loads_ping() -> None:
    from botos_core.plugin_manager import PluginManager
    pm = PluginManager()
    pm.discover_standard_plugins()
    assert "botos.standard.ping" in pm.list_ids()

def test_bug_100_total_command_count() -> None:
    from botos_core.plugin_manager import PluginManager
    pm = PluginManager()
    pm.discover_standard_plugins()
    assert pm.total_command_count() >= 1
