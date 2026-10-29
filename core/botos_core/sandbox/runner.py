"""Isolated execution for user/plugin code.

Validation is done in-process (AST whitelist), execution happens inside a
short-lived worker subprocess so runaway code (infinite loops, huge
allocations, deep recursion) is killed by timeout regardless of whether the
generated code yields to the event loop.
"""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import dataclass
from typing import Any

from botos_core.constants import (
    SANDBOX_MAX_MEMORY_MB,
    SANDBOX_TIMEOUT_SECONDS,
    SANDBOX_WORKER_EXIT_TIMEOUT,
)
from botos_core.sandbox.validation import validate_source
from botos_core.sandbox.wrapper import SandboxInteractionContext


@dataclass
class SandboxResult:
    ok: bool
    value: Any = None
    error: str | None = None


class SandboxRunner:
    timeout_seconds: float = SANDBOX_TIMEOUT_SECONDS
    max_memory_mb: int = SANDBOX_MAX_MEMORY_MB

    def validate_python_source(self, source: str) -> SandboxResult:

        error = validate_source(source)
        if error:
            return SandboxResult(ok=False, error=error)
        return SandboxResult(ok=True, value={"validated": True})

    def _payload(
        self,
        source: str,
        handler_name: str,
        ctx_data: dict[str, Any],
    ) -> bytes:
        payload = json.dumps(
            {
                "source": source,
                "handler": handler_name,
                "ctx": ctx_data or {},
            }
        )
        return payload.encode("utf-8")

    async def _run_worker(self, payload: bytes) -> SandboxResult:
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-m",
            "botos_core.sandbox.worker",
            str(self.max_memory_mb),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            out, err = await asyncio.wait_for(
                proc.communicate(payload),
                timeout=self.timeout_seconds,
            )
        except TimeoutError:
            proc.kill()
            await proc.wait()
            return SandboxResult(ok=False, error="timeout")
        if proc.returncode == SANDBOX_WORKER_EXIT_TIMEOUT:
            return SandboxResult(ok=False, error="worker exit: timeout")
        if proc.returncode != 0:
            detail = (err.decode("utf-8", "replace") or "unknown error").strip()
            return SandboxResult(ok=False, error=f"runtime error: {detail[-500:]}")
        try:
            data = json.loads(out.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return SandboxResult(ok=False, error="worker produced invalid output")
        if not data.get("ok", False):
            return SandboxResult(ok=False, error=str(data.get("error", "unknown error")))
        return SandboxResult(
            ok=True,
            value={
                "replies": data.get("replies", []),
                "channel_sends": data.get("channel_sends", []),
            },
        )

    async def run_plugin_command(
        self,
        manifest: dict[str, Any],
        command_name: str,
        ctx: SandboxInteractionContext,
    ) -> SandboxResult:
        entrypoint = manifest.get("entrypoint") or {}
        source = str(entrypoint.get("generated_code", ""))
        validated = self.validate_python_source(source)
        if not validated.ok:
            return validated
        ctx_data = ctx.to_payload()
        ctx_data["config"] = dict(manifest.get("plugin_config") or {})
        payload = self._payload(source, "on_command_" + command_name.replace("-", "_"), ctx_data)
        result = await self._run_worker(payload)
        if not result.ok:
            return result
        return SandboxResult(ok=True, value=result.value)

    async def run_plugin_event(
        self,
        manifest: dict[str, Any],
        event_name: str,
        member: Any,
        plugin_config: dict[str, Any] | None = None,
    ) -> SandboxResult:
        if event_name not in (manifest.get("events") or []):
            return SandboxResult(ok=False, error=f"event {event_name} not declared in manifest")
        entrypoint = manifest.get("entrypoint") or {}
        source = str(entrypoint.get("generated_code", ""))
        validated = self.validate_python_source(source)
        if not validated.ok:
            return validated
        ctx_data: dict[str, Any] = {
            "member": {
                "name": str(getattr(member, "name", "unknown")),
                "id": str(getattr(member, "id", "")),
            },
            "config": dict(plugin_config or {}),
        }
        payload = self._payload(source, event_name, ctx_data)
        result = await self._run_worker(payload)
        if not result.ok:
            return result
        return SandboxResult(ok=True, value=result.value)
