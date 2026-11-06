"""TAQVO API configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """Load API settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    bot_token: SecretStr = Field(
        validation_alias="BOT_TOKEN"
    )

    database_url: SecretStr = Field(
        validation_alias="DATABASE_URL"
    )

    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
    )

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: object) -> object:
        """Convert common PostgreSQL URLs to the asyncpg format."""

        if not isinstance(value, str):
            return value

        value = value.strip()

        if value.startswith("postgres://"):
            return value.replace(
                "postgres://",
                "postgresql+asyncpg://",
                1,
            )

        if value.startswith("postgresql://"):
            return value.replace(
                "postgresql://",
                "postgresql+asyncpg://",
                1,
            )

        return value


@lru_cache(maxsize=1)
def get_api_settings() -> APISettings:
    """Return cached API settings."""
    return APISettings()
