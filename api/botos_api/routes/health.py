"""Health and stats — rds9team OPERATIONS convention."""

from __future__ import annotations

import time

from fastapi import APIRouter

router = APIRouter(tags=["health"])

_started_at = time.time()


@router.get("/health")
async def health_root() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/health")
async def health_api() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/api/stats")
async def stats() -> dict[str, str | int | float]:
    return {
        "status": "ok",
        "service": "botos-api",
        "uptime_seconds": round(time.time() - _started_at, 1),
        "guilds_managed": 0,
    }
