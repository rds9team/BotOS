"""API settings from environment."""

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from botos_api.repo_root import repo_root


class ApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(repo_root() / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    botos_host: str = "0.0.0.0"
    botos_port: int = Field(default=8000, ge=1, le=65535)
    botos_reload: bool = False
    database_url: str = "sqlite+aiosqlite:///data/botos.db"
    jwt_secret: str = Field(default="replace_this_with_a_secure_random_key_32chars", min_length=16)
    discord_client_id: str = ""
    discord_client_secret: str = ""
    discord_redirect_uri: str = "http://localhost:8000/api/auth/discord/callback"
    jwt_expires_minutes: int = Field(default=60 * 24 * 7, ge=5, le=60 * 24 * 30)

    @field_validator("database_url")
    @classmethod
    def database_url_not_blank(cls, value: str) -> str:
        if not value.strip():
            msg = "DATABASE_URL must not be empty"
            raise ValueError(msg)
        return value.strip()

    @field_validator("jwt_secret")
    @classmethod
    def jwt_secret_not_placeholder_in_prod(cls, value: str) -> str:
        if value.strip() == "replace_this_with_a_secure_random_key_32chars":
            return value
        return value


def load_settings() -> ApiSettings:
    return ApiSettings()
