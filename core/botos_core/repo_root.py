"""Repository root (BotOS/)."""

from pathlib import Path


def repo_root() -> Path:
    # core/botos_core/repo_root.py -> parents[2]
    return Path(__file__).resolve().parents[2]
