"""Sandbox worker subprocess: runs one plugin handler and returns actions.

Usage (spawned by SandboxRunner):
    python -m botos_core.sandbox.worker <max_memory_mb>

stdin:  JSON {"source": ..., "handler": ..., "ctx": {...}}
stdout: JSON {"ok": bool, "error": str?, "replies": [...], "channel_sends": [...]}
exit codes: 0 completed (validation or handler outcome), 1 runtime error/crash.
"""

from __future__ import annotations

import asyncio
import builtins
import importlib
import inspect
import json
import resource
import sys

EXIT_RUNTIME_ERROR = 1

from botos_core.constants import ALLOWED_IMPORT_MODULES  # noqa: E402
from botos_core.sandbox.validation import validate_source  # noqa: E402

_SAFE_BUILTINS = {
    name: getattr(builtins, name)
    for name in (
        "None",
        "True",
        "False",
        "str",
        "int",
        "float",
        "bool",
        "len",
        "range",
        "min",
        "max",
        "sum",
        "abs",
        "round",
        "dict",
        "list",
        "tuple",
        "set",
        "frozenset",
        "sorted",
        "reversed",
        "enumerate",
        "zip",
        "any",
        "all",
        "isinstance",
        "getattr",
        "hasattr",
        "print",
    )
    if hasattr(builtins, name)
}


def _safe_import(name: str, _globals=None, _locals=None, fromlist=(), level=0):
    root = str(name).split(".", 1)[0]
    if root not in ALLOWED_IMPORT_MODULES:
        raise ImportError(f"import of {root!r} is not allowed in sandbox")
    return importlib.import_module(str(name))


_RESULT: dict = {"ok": True, "replies": [], "channel_sends": []}


class _PluginCtx:
    def __init__(self, data: dict) -> None:
        self.user = data.get("user") or {}
        self.member = data.get("member") or {}
        self.guild = data.get("guild") or {}
        self.channel = data.get("channel") or {}
        self.config = data.get("config") or {}

    async def reply(self, content: str, *, ephemeral: bool = False) -> None:
        _RESULT["replies"].append(
            {"content": str(content)[:2000], "ephemeral": bool(ephemeral)}
        )

    async def send_to_channel(self, channel_id: str, content: str) -> None:
        _RESULT["channel_sends"].append(
            {"channel_id": str(channel_id), "content": str(content)[:2000]}
        )


async def _call(handler, ctx) -> None:
    if inspect.iscoroutinefunction(handler):
        await handler(ctx)
    else:
        ctx_result = handler(ctx)
        if asyncio.iscoroutine(ctx_result):
            await ctx_result


def main() -> int:
    try:
        memory_mb = int(sys.argv[1])
    except (IndexError, ValueError):
        memory_mb = 64
    try:
        limit_bytes = memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (limit_bytes, limit_bytes))
    except (OSError, ValueError):
        pass

    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError as exc:
        _RESULT["ok"] = False
        _RESULT["error"] = f"bad payload: {exc.msg}"
        return _emit(EXIT_RUNTIME_ERROR)

    source = str(payload.get("source", ""))
    handler_name = str(payload.get("handler", ""))
    ctx_data = payload.get("ctx") or {}

    error = validate_source(source)
    if error:
        _RESULT["ok"] = False
        _RESULT["error"] = error
        return _emit(0)

    namespace: dict = {"__builtins__": {**_SAFE_BUILTINS, "__import__": _safe_import}}
    try:
        exec(compile(source, "<plugin>", "exec"), namespace, namespace)
    except BaseException as exc:
        _RESULT["ok"] = False
        _RESULT["error"] = f"load error: {exc}"
        return _emit(EXIT_RUNTIME_ERROR)

    handler = namespace.get(handler_name)
    if handler is None or not callable(handler):
        _RESULT["ok"] = False
        _RESULT["error"] = "missing handler"
        return _emit(0)

    ctx = _PluginCtx(ctx_data)
    try:
        if not inspect.iscoroutinefunction(handler):
            _RESULT["ok"] = False
            _RESULT["error"] = "handler must be async def"
            return _emit(0)
        asyncio.run(handler(ctx))
    except MemoryError:
        _RESULT["ok"] = False
        _RESULT["error"] = "memory limit exceeded"
        return _emit(EXIT_RUNTIME_ERROR)
    except BaseException as exc:
        _RESULT["ok"] = False
        _RESULT["error"] = f"runtime error: {exc}"
        return _emit(EXIT_RUNTIME_ERROR)
    return _emit(0)


def _emit(code: int) -> int:
    sys.stdout.write(json.dumps(_RESULT))
    sys.stdout.write("\n")
    sys.stdout.flush()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
