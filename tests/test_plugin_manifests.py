"""Tests for standard plugin manifests and sandboxed handler execution."""

from __future__ import annotations

import pytest

from botos_core.plugin_manager import PluginManager
from botos_core.repo_root import repo_root
from botos_core.sandbox.runner import SandboxRunner
from botos_core.sandbox.wrapper import SandboxInteractionContext


class FakeResponse:
    def __init__(self) -> None:
        self.is_done = False
        self.content: str | None = None
        self.ephemeral: bool | None = None

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


class FakeMember:
    def __init__(self, name: str, member_id: str = "1") -> None:
        self.name = name
        self.id = int(member_id)


@pytest.fixture(scope="module")
def standard_manifests() -> dict[str, dict]:
    manager = PluginManager(plugins_root=repo_root() / "plugins")
    manager.discover_standard_plugins()
    return {pid: manager.get(pid).raw for pid in manager.list_ids()}  # type: ignore[union-attr]


def test_plug01_standard_command_manifests_wellformed(standard_manifests) -> None:
    for pid in ("botos.standard.ping", "botos.standard.fortune", "botos.standard.dice"):
        assert pid in standard_manifests
        manifest = standard_manifests[pid]
        assert isinstance(manifest["commands"], list) and manifest["commands"]
        command_def = manifest["commands"][0]
        assert 1 <= len(str(command_def["name"])) <= 32
        assert len(str(command_def["description"])) <= 100
        assert command_def["name"].islower()


@pytest.mark.asyncio
async def test_plug01_fortune_replies_fortune_result(standard_manifests) -> None:
    manifest = standard_manifests["botos.standard.fortune"]
    fake = FakeInteraction()
    result = await SandboxRunner().run_plugin_command(
        manifest,
        "fortune",
        SandboxInteractionContext(fake),  # type: ignore[arg-type]
    )
    assert result.ok is True
    replies = result.value["replies"]
    assert len(replies) == 1
    assert replies[0]["content"] in {"大吉", "吉", "中吉", "小吉", "凶", "大凶"}
    assert replies[0]["ephemeral"] is True


@pytest.mark.asyncio
async def test_plug01_dice_replies_1_to_6(standard_manifests) -> None:
    manifest = standard_manifests["botos.standard.dice"]
    fake = FakeInteraction()
    result = await SandboxRunner().run_plugin_command(
        manifest,
        "dice",
        SandboxInteractionContext(fake),  # type: ignore[arg-type]
    )
    assert result.ok is True
    replies = result.value["replies"]
    assert replies[0]["content"] in {"1", "2", "3", "4", "5", "6"}


# ---------- PLUG-02: welcome (event-driven) ----------


def test_plug02_welcome_manifest_contract(standard_manifests) -> None:
    manifest = standard_manifests["botos.standard.welcome"]
    assert manifest["events"] == ["on_member_join"]
    schema = manifest["config_schema"]
    assert "channel_id" in schema
    assert "message" in schema
    assert schema["channel_id"]["required"] is True


@pytest.mark.asyncio
async def test_plug02_welcome_handler_queues_channel_send(standard_manifests) -> None:
    manifest = dict(standard_manifests["botos.standard.welcome"])
    manifest["plugin_config"] = {"channel_id": "12345", "message": "ようこそ、{user} さん!"}
    member = FakeMember("karumaru")
    result = await SandboxRunner().run_plugin_event(
        manifest,
        "on_member_join",
        member,
        manifest["plugin_config"],
    )
    assert result.ok is True
    sends = result.value["channel_sends"]
    assert sends == [{"channel_id": "12345", "content": "ようこそ、karumaru さん!"}]


@pytest.mark.asyncio
async def test_plug02_undeclared_event_is_rejected(standard_manifests) -> None:
    manifest = dict(standard_manifests["botos.standard.welcome"])
    manifest["events"] = []
    result = await SandboxRunner().run_plugin_event(
        manifest,
        "on_member_join",
        FakeMember("bob"),
        {},
    )
    assert result.ok is False
    assert "not declared" in (result.error or "")


@pytest.mark.asyncio
async def test_plug02_channel_id_is_validated_before_discord_send(standard_manifests) -> None:
    """config の channel_id が非数字なら dispatch 側で ValueError になる。"""
    from botos_core.event_dispatch import _send_to_guild_channel

    class _Guild:
        def get_channel_or_thread(self, channel_id):  # noqa: ANN202
            return None

    with pytest.raises(ValueError, match="invalid channel id"):
        await _send_to_guild_channel(_Guild(), "not-a-number", "hello")

    with pytest.raises(ValueError, match="channel not found"):
        await _send_to_guild_channel(_Guild(), "999", "hello")
