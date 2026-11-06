from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """TAQVO BOT configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    bot_token: SecretStr = Field(validation_alias="BOT_TOKEN")

    channel_username: str = Field(
        default="@hakiymqalb",
        validation_alias="CHANNEL_USERNAME",
    )

    mini_app_url: str | None = Field(
        default=None,
        validation_alias="MINI_APP_URL",
    )

    backend_base_url: str | None = Field(
        default=None,
        validation_alias="BACKEND_BASE_URL",
    )

    timezone: str = Field(
        default="UTC",
        validation_alias="DEFAULT_TIMEZONE",
    )

    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
    )

    @field_validator("channel_username")
    @classmethod
    def validate_channel_username(cls, value: str) -> str:
        value = value.strip()

        if not value.startswith("@") or len(value) < 2:
            raise ValueError(
                "CHANNEL_USERNAME must start with @"
            )

        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
