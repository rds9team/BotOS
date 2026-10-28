"""SQLAlchemy models — aligned with `docs/database-schema.md` (skeleton)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    # manifest / content JSON columns — add when migrations are introduced


class GuildPlugin(Base):
    __tablename__ = "guild_plugins"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    guild_id: Mapped[str] = mapped_column(String(32), ForeignKey("guilds.id"))
    plugin_id: Mapped[str] = mapped_column(String(64), ForeignKey("plugins.id"))
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    installed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
