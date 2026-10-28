"""Isolated execution for user/plugin code. See `docs/sandbox-spec.md`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SandboxResult:
    ok: bool
    value: Any = None
    error: str | None = None


class SandboxRunner:
    """Placeholder runner — always returns not implemented."""

    async def run_handler(self, handler_name: str, **kwargs: Any) -> SandboxResult:
        _ = handler_name, kwargs
        return SandboxResult(ok=False, error="SandboxRunner not implemented")
