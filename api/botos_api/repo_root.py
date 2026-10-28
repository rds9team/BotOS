"""Repository root (BotOS/)."""

from pathlib import Path


def repo_root() -> Path:
    # api/botos_api/repo_root.py -> parents[2]
    return Path(__file__).resolve().parents[2]
