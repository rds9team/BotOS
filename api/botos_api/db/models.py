"""SQLAlchemy models — aligned with `docs/database-schema.md`."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    discord_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100))
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class UserOAuthToken(Base):
    __tablename__ = "user_oauth_tokens"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), primary_key=True)
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Guild(Base):
    __tablename__ = "guilds"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    icon_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    max_commands: Mapped[int] = mapped_column(Integer, default=30)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class Plugin(Base):
    __tablename__ = "plugins"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_id: Mapped[str | None] = mapped_column(String(36), ForeignKey("users.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(20))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    manifest: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    content: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class GuildPlugin(Base):
    __tablename__ = "guild_plugins"
    __table_args__ = (UniqueConstraint("guild_id", "plugin_id", name="uq_guild_plugin"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    guild_id: Mapped[str] = mapped_column(String(32), ForeignKey("guilds.id"))
    plugin_id: Mapped[str] = mapped_column(String(64), ForeignKey("plugins.id"))
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    config: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class GuildSyncRequest(Base):
    __tablename__ = "guild_sync_requests"

    guild_id: Mapped[str] = mapped_column(String(32), ForeignKey("guilds.id"), primary_key=True)
    requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )


class CommandQuotaRequest(Base):
    __tablename__ = "command_quota_requests"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    guild_id: Mapped[str] = mapped_column(String(32), ForeignKey("guilds.id"))
    requested_by: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    requested_quota: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
