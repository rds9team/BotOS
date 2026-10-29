"""Tests for OAuth JWT, sandbox execution, and guild plugin install."""

from __future__ import annotations

import pytest

from botos_api.auth.jwt_tokens import create_access_token, decode_access_token
from botos_core.sandbox.runner import SandboxRunner
from botos_core.sandbox.wrapper import SandboxInteractionContext


def test_jwt_roundtrip() -> None:
    token = create_access_token(user_id="user-1", discord_id="999")
    payload = decode_access_token(token)
    assert payload["sub"] == "user-1"
    assert payload["discord_id"] == "999"


def test_oauth_state_roundtrip() -> None:
    from botos_api.auth.discord_oauth import create_oauth_state, verify_oauth_state

    state = create_oauth_state()
    assert verify_oauth_state(state) is True
    assert verify_oauth_state("tampered") is False


@pytest.mark.asyncio
async def test_sandbox_runs_ping_handler() -> None:
    class FakeResponse:
        is_done = False

        async def send_message(self, content: str, ephemeral: bool = False) -> None:
            self.content = content
            self.ephemeral = ephemeral

    class FakeFollowup:
        async def send(self, content: str, ephemeral: bool = False) -> None:
            pass

    class FakeInteraction:
        def __init__(self) -> None:
            self.response = FakeResponse()
            self.followup = FakeFollowup()
            self.user = object()
            self.channel = None
            self.guild = None

    manifest = {
        "entrypoint": {
            "generated_code": (
                "async def on_command_ping(ctx):\n"
                "    await ctx.reply('pong', ephemeral=True)\n"
            )
        }
    }
    fake = FakeInteraction()
    runner = SandboxRunner()
    ctx = SandboxInteractionContext(fake)  # type: ignore[arg-type]
    result = await runner.run_plugin_command(manifest, "ping", ctx)
    assert result.ok is True
    replies = result.value["replies"]
    assert replies[0]["content"] == "pong"
    assert replies[0]["ephemeral"] is True


@pytest.mark.asyncio
async def test_plugin_handler_timeout_reports_error() -> None:
    class FakeResponse:
        is_done = False

        async def send_message(self, content: str, ephemeral: bool = False) -> None:
            self.content = content
            self.ephemeral = ephemeral

    class FakeFollowup:
        async def send(self, content: str, ephemeral: bool = False) -> None:
            pass

    class FakeInteraction:
        def __init__(self) -> None:
            self.response = FakeResponse()
            self.followup = FakeFollowup()
            self.user = object()
            self.channel = None
            self.guild = None

    manifest = {
        "entrypoint": {
            "generated_code": (
                "async def on_command_ping(ctx):\n"
                "    while True:\n"
                "        pass\n"
            )
        }
    }
    runner = SandboxRunner()
    runner.timeout_seconds = 0.5
    ctx = SandboxInteractionContext(FakeInteraction())  # type: ignore[arg-type]
    result = await runner.run_plugin_command(manifest, "ping", ctx)
    assert result.ok is False
    assert result.error == "timeout"
