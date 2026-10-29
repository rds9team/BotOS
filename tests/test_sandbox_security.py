"""Sandbox escape / abuse attack suites (QA-01).

Each case runs malicious generated_code through the same SandboxRunner
pipeline the core uses for plugins, and verifies it is blocked.
"""

from __future__ import annotations

import pytest

from botos_core.sandbox.runner import SandboxRunner
from botos_core.sandbox.wrapper import SandboxInteractionContext


class FakeResponse:
    def __init__(self) -> None:
        self.is_done = False

    async def send_message(self, content: str, ephemeral: bool = False) -> None:
        pass


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


def _manifest(source: str) -> dict:
    return {
        "id": "test.malicious",
        "entrypoint": {"generated_code": source},
        "commands": [{"name": "ping"}],
        "events": ["on_member_join"],
    }


def _as(header: str, body: str) -> str:
    return header + "async def on_command_ping(ctx):\n" + body


async def _run_command(source: str, timeout: float = 0.5) -> object:
    runner = SandboxRunner()
    runner.timeout_seconds = timeout
    return await runner.run_plugin_command(
        _manifest(source),
        "ping",
        SandboxInteractionContext(FakeInteraction()),  # type: ignore[arg-type]
    )


# ---------------- AST validation blocks (import / dunder / builtin) ----------------


@pytest.mark.parametrize(
    ("attack_id", "source"),
    [
        ("A01_import_os", _as("import os\n", "    os.system('true')\n")),
        ("A02_from_os_import_exit", _as("from os import _exit\n", "    _exit()\n")),
        ("A03_import_subprocess", _as("import subprocess\n", "    subprocess.run(['ls'])\n")),
        ("A04_import_sys_getframe", _as("import sys\n", "    f = sys._getframe(1)\n")),
        ("A05_import_ctypes", _as("import ctypes\n", "    libc = ctypes.CDLL('libc.so.6')\n")),
        ("A06_import_socket", _as("import socket\n", "    s = socket.socket()\n")),
        ("A07_import_importlib", _as("import importlib\n", "    importlib.import_module('os')\n")),
        ("A08_import_threading", _as("import threading\n", "    threading.Thread()\n")),
        ("A09_eval_call", _as("", "    eval(\"__import__('os').system('true')\")\n")),
        ("A10_exec_call", _as("", "    exec(\"import os\")\n")),
        ("A11_direct_dunder_import_call", _as("", "    __import__('os')\n")),
        ("A12_class_subclasses_escape",
            "async def on_command_ping(ctx):\n"
            "    sc = ().__class__.__base__.__subclasses__()\n"),
        ("A13_func_globals_access", (
            "def helper() -> None:\n"
            "    return None\n"
            "async def on_command_ping(ctx):\n"
            "    g = helper.__globals__\n"
        )),
        ("A14_builtins_rebind_attempt", (
            "async def on_command_ping(ctx):\n"
            "    __builtins__ = {}\n"
        )),
        ("A15_frame_object_traversal", (
            "async def on_command_ping(ctx):\n"
            "    code = ctx.reply.__code__\n"
        )),
    ],
)
@pytest.mark.asyncio
async def test_attack_blocked(attack_id: str, source: str) -> None:
    result = await _run_command(source)
    assert result.ok is False, f"{attack_id} was NOT blocked"
    assert result.error


# ---------------- runtime level catch-alls ----------------


@pytest.mark.asyncio
async def test_open_is_not_available_in_namespace() -> None:
    source = "async def on_command_ping(ctx):\n    open('/etc/passwd')\n"
    result = await _run_command(source)
    assert result.ok is False
    assert "runtime error" in (result.error or "")


@pytest.mark.asyncio
async def test_runaway_recursion_is_caught_at_runtime() -> None:
    source = (
        "async def on_command_ping(ctx):\n"
        "    def boom(n):\n"
        "        return boom(n + 1)\n"
        "    boom(0)\n"
    )
    result = await _run_command(source)
    assert result.ok is False
    assert result.error


@pytest.mark.asyncio
async def test_infinite_async_loop_hits_timeout() -> None:
    source = (
        "async def on_command_ping(ctx):\n"
        "    while True:\n"
        "        await ctx.reply('x')\n"
    )
    result = await _run_command(source, timeout=0.2)
    assert result.ok is False
    assert result.error == "timeout"


@pytest.mark.asyncio
async def test_sync_handler_is_rejected() -> None:
    source = "def on_command_ping(ctx):\n    return 1\n"
    result = await _run_command(source)
    assert result.ok is False
    assert result.error == "handler must be async def"


@pytest.mark.asyncio
async def test_huge_memory_allocation_is_contained_by_timeout() -> None:
    source = "async def on_command_ping(ctx):\n    blob = 'A' * (10 ** 12)\n"
    result = await _run_command(source)
    assert result.ok is False


@pytest.mark.asyncio
async def test_missing_handler_reports_error() -> None:
    source = (
        "async def some_other_name(ctx):\n"
        "    return 1\n"
    )
    result = await _run_command(source)
    assert result.ok is False
    assert result.error == "missing handler"


@pytest.mark.asyncio
async def test_allowed_random_import_still_works() -> None:
    source = (
        "import random\n"
        "async def on_command_ping(ctx):\n"
        "    await ctx.reply(str(random.randint(1, 6)), ephemeral=True)\n"
    )
    result = await _run_command(source)
    assert result.ok is True
