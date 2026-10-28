"""Isolated execution for user/plugin code. See `docs/sandbox-spec.md`."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any

from botos_core.constants import SANDBOX_MAX_MEMORY_MB, SANDBOX_TIMEOUT_SECONDS

FORBIDDEN_IMPORTS = frozenset(
    {
        "os",
        "sys",
        "subprocess",
        "socket",
        "ctypes",
        "threading",
        "multiprocessing",
        "importlib",
    }
)


@dataclass
class SandboxResult:
    ok: bool
    value: Any = None
    error: str | None = None


class SandboxRunner:
    """Validates Python snippets before execution (execution still TODO)."""

    timeout_seconds: float = SANDBOX_TIMEOUT_SECONDS
    max_memory_mb: int = SANDBOX_MAX_MEMORY_MB

    def validate_python_source(self, source: str) -> SandboxResult:
        if not source.strip():
            return SandboxResult(ok=False, error="empty source")
        try:
            tree = ast.parse(source, mode="exec")
        except SyntaxError as exc:
            return SandboxResult(ok=False, error=f"syntax error: {exc.msg}")
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in FORBIDDEN_IMPORTS:
                        return SandboxResult(ok=False, error=f"forbidden import: {root}")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_IMPORTS:
                        return SandboxResult(ok=False, error=f"forbidden import: {root}")
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {"eval", "exec", "__import__"}:
                    return SandboxResult(ok=False, error=f"forbidden builtin: {node.func.id}")
        return SandboxResult(ok=True, value={"nodes": len(list(ast.walk(tree)))})

    async def run_handler(self, handler_name: str, **kwargs: Any) -> SandboxResult:
        if not handler_name.strip():
            return SandboxResult(ok=False, error="handler_name required")
        return SandboxResult(ok=False, error="SandboxRunner execution not implemented")
