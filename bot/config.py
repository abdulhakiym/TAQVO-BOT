
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for TAQVO PRO MAX."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="TAQVO PRO MAX", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=False, alias="DEBUG")
    app_host: str = Field(default="0.0.0.0", alias="APP_HOST")
    app_port: int = Field(default=8000, alias="APP_PORT")

    # Telegram
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    bot_username: str = Field(default="", alias="BOT_USERNAME")
    channel_username: str = Field(
        default="@hakiymqalb",
        alias="CHANNEL_USERNAME",
    )

    # Mini App
    webapp_url: str = Field(default="", alias="WEBAPP_URL")
    app_base_url: str = Field(default="", alias="APP_BASE_URL")

    # Database
    database_url: str = Field(
        default="",
        alias="DATABASE_URL",
    )

    # Security
    secret_key: str = Field(default="", alias="SECRET_KEY")
    webapp_initdata_max_age: int = Field(
        default=86400,
        alias="WEBAPP_INITDATA_MAX_AGE",
    )

    # Timezone
    default_timezone: str = Field(
        default="Asia/Tashkent",
        alias="DEFAULT_TIMEZONE",
    )

    # Prayer times
    prayer_api_base_url: str = Field(
        default="https://api.aladhan.com/v1",
        alias="PRAYER_API_BASE_URL",
    )
    prayer_calculation_method: int = Field(
        default=3,
        alias="PRAYER_CALCULATION_METHOD",
    )
    prayer_asr_method: int = Field(
        default=0,
        alias="PRAYER_ASR_METHOD",
    )

    # Reminders
    prayer_reminders_enabled: bool = Field(
        default=True,
        alias="PRAYER_REMINDERS_ENABLED",
    )
    prayer_reminder_minutes: int = Field(
        default=5,
        alias="PRAYER_REMINDER_MINUTES",
    )
    akhirah_reminders_enabled: bool = Field(
        default=True,
        alias="AKHIRAH_REMINDERS_ENABLED",
    )
    morning_reminder_time: str = Field(
        default="08:00",
        alias="MORNING_REMINDER_TIME",
    )
    evening_reminder_time: str = Field(
        default="20:00",
        alias="EVENING_REMINDER_TIME",
    )

    # Scheduler
    scheduler_enabled: bool = Field(
        default=True,
        alias="SCHEDULER_ENABLED",
    )

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # AI
    ai_enabled: bool = Field(default=False, alias="AI_ENABLED")
    ai_api_key: str = Field(default="", alias="AI_API_KEY")
    ai_model: str = Field(default="", alias="AI_MODEL")

    # Knowledge base
    knowledge_search_enabled: bool = Field(
        default=True,
        alias="KNOWLEDGE_SEARCH_ENABLED",
    )
    vector_search_enabled: bool = Field(
        default=False,
        alias="VECTOR_SEARCH_ENABLED",
    )

    # Admin
    admin_telegram_ids: str = Field(
        default="",
        alias="ADMIN_TELEGRAM_IDS",
    )

    # CORS
    cors_origins: str = Field(
        default="http://localhost:8000,http://localhost:3000",
        alias="CORS_ORIGINS",
    )

    @property
    def admin_ids(self) -> List[int]:
        """Convert comma-separated admin IDs into integers."""
        result = []

        for value in self.admin_telegram_ids.split(","):
            value = value.strip()

            if value:
                try:
                    result.append(int(value))
                except ValueError:
                    raise ValueError(
                        f"Invalid Telegram admin ID: {value}"
                    )

        return result

    @property
    def allowed_origins(self) -> List[str]:
        """Convert CORS origins into a list."""
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()
