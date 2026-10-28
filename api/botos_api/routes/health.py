"""Health and stats — rds9team OPERATIONS convention."""

from __future__ import annotations

import time

from fastapi import APIRouter, Response
from sqlalchemy import func, select

from botos_api.db.models import Guild
from botos_api.db.session import get_engine

router = APIRouter(tags=["health"])

_started_at: float | None = None


def set_started_at(when: float) -> None:
    global _started_at
    _started_at = when


def _uptime_seconds() -> float:
    if _started_at is None:
        return 0.0
    return round(time.time() - _started_at, 1)


def _no_cache_headers() -> dict[str, str]:
    return {"Cache-Control": "no-store"}


@router.get("/health")
async def health_root(response: Response) -> dict[str, str]:
    for key, value in _no_cache_headers().items():
        response.headers[key] = value
    return {"status": "ok"}


@router.get("/api/health")
async def health_api(response: Response) -> dict[str, str]:
    for key, value in _no_cache_headers().items():
        response.headers[key] = value
    return {"status": "ok"}


@router.get("/api/stats")
async def stats(response: Response) -> dict[str, str | int | float]:
    for key, value in _no_cache_headers().items():
        response.headers[key] = value
    guilds_managed = 0
    try:
        from sqlalchemy.exc import SQLAlchemyError
        from sqlalchemy.ext.asyncio import async_sessionmaker

        engine = get_engine()
        session_factory = async_sessionmaker(engine, expire_on_commit=False)
        async with session_factory() as session:
            guilds_managed = int(await session.scalar(select(func.count()).select_from(Guild)) or 0)
    except (OSError, SQLAlchemyError):
        guilds_managed = 0
    return {
        "status": "ok",
        "service": "botos-api",
        "uptime_seconds": _uptime_seconds(),
        "guilds_managed": guilds_managed,
    }
