"""AST-level validation shared by SandboxRunner and the sandbox worker."""

from __future__ import annotations

import ast

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


def validate_source(source: str) -> str | None:
    """Return an error message if the source is not allowed, else None."""

    if not source.strip():
        return "empty source"
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        return f"syntax error: {exc.msg}"
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in FORBIDDEN_IMPORTS:
                    return f"forbidden import: {root}"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root = node.module.split(".", 1)[0]
                if root in FORBIDDEN_IMPORTS:
                    return f"forbidden import: {root}"
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in {"eval", "exec", "__import__"}:
                return f"forbidden builtin: {node.func.id}"
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("__") and node.attr.endswith("__"):
                return f"forbidden dunder attribute: {node.attr}"
        elif isinstance(node, ast.Name):
            if node.id.startswith("__") and node.id.endswith("__"):
                return f"forbidden dunder name: {node.id}"
    return None
