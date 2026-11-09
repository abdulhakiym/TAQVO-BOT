"""TAQVO PRO MAX central configuration."""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        populate_by_name=True,
    )

    # --------------------------------------------------
    # APPLICATION
    # --------------------------------------------------

    app_name: str = Field(
        default="TAQVO PRO MAX",
        alias="APP_NAME",
    )

    app_env: str = Field(
        default="development",
        alias="APP_ENV",
    )

    debug: bool = Field(
        default=False,
        alias="DEBUG",
    )

    app_host: str = Field(
        default="0.0.0.0",
        alias="APP_HOST",
    )

    app_port: int = Field(
        default=8000,
        alias="APP_PORT",
    )

    # --------------------------------------------------
    # TELEGRAM BOT
    # --------------------------------------------------

    bot_token: SecretStr = Field(
        default=SecretStr(""),
        alias="BOT_TOKEN",
    )

    bot_username: str = Field(
        default="",
        alias="BOT_USERNAME",
    )

    channel_username: str = Field(
        default="@hakiymqalb",
        alias="CHANNEL_USERNAME",
    )

    # --------------------------------------------------
    # TELEGRAM MINI APP
    # --------------------------------------------------

    webapp_url: str = Field(
        default="",
        alias="WEBAPP_URL",
    )

    app_base_url: str = Field(
        default="",
        alias="APP_BASE_URL",
    )

    @property
    def mini_app_url(self) -> str:
        """Compatibility with existing Mini App keyboards."""
        return self.webapp_url.strip()

    # --------------------------------------------------
    # DATABASE
    # --------------------------------------------------

    database_url: str = Field(
        default="",
        alias="DATABASE_URL",
    )

    # --------------------------------------------------
    # SECURITY
    # --------------------------------------------------

    secret_key: SecretStr = Field(
        default=SecretStr(""),
        alias="SECRET_KEY",
    )

    webapp_initdata_max_age: int = Field(
        default=86400,
        alias="WEBAPP_INITDATA_MAX_AGE",
    )

    # --------------------------------------------------
    # TIMEZONE
    # --------------------------------------------------

    default_timezone: str = Field(
        default="Asia/Tashkent",
        alias="DEFAULT_TIMEZONE",
    )

    # --------------------------------------------------
    # PRAYER TIMES
    # --------------------------------------------------

    prayer_api_base_url: str = Field(
        default="https://api.aladhan.com/v1",
        alias="PRAYER_API_BASE_URL",
    )

    prayer_calculation_method: int = Field(
        default=3,
        alias="PRAYER_CALCULATION_METHOD",
    )

    # 0 = Shafi'i, Maliki, Hanbali
    # 1 = Hanafi
    prayer_asr_method: int = Field(
        default=1,
        alias="PRAYER_ASR_METHOD",
    )

    # --------------------------------------------------
    # REMINDERS
    # --------------------------------------------------

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

    # --------------------------------------------------
    # SCHEDULER
    # --------------------------------------------------

    scheduler_enabled: bool = Field(
        default=True,
        alias="SCHEDULER_ENABLED",
    )

    # --------------------------------------------------
    # LOGGING
    # --------------------------------------------------

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    # --------------------------------------------------
    # AI
    # --------------------------------------------------

    ai_enabled: bool = Field(
        default=False,
        alias="AI_ENABLED",
    )

    ai_api_key: SecretStr = Field(
        default=SecretStr(""),
        alias="AI_API_KEY",
    )

    ai_model: str = Field(
        default="",
        alias="AI_MODEL",
    )

    # --------------------------------------------------
    # KNOWLEDGE BASE
    # --------------------------------------------------

    knowledge_search_enabled: bool = Field(
        default=True,
        alias="KNOWLEDGE_SEARCH_ENABLED",
    )

    vector_search_enabled: bool = Field(
        default=False,
        alias="VECTOR_SEARCH_ENABLED",
    )

    # --------------------------------------------------
    # ADMIN
    # --------------------------------------------------

    admin_telegram_ids: str = Field(
        default="",
        alias="ADMIN_TELEGRAM_IDS",
    )

    @property
    def admin_ids(self) -> list[int]:
        """Convert comma-separated admin IDs to integers."""

        result: list[int] = []

        for value in self.admin_telegram_ids.split(","):
            value = value.strip()

            if not value:
                continue

            try:
                result.append(int(value))
            except ValueError as exc:
                raise ValueError(
                    f"Invalid Telegram admin ID: {value}"
                ) from exc

        return result

    # --------------------------------------------------
    # CORS
    # --------------------------------------------------

    cors_origins: str = Field(
        default=(
            "http://localhost:8000,"
            "http://localhost:3000"
        ),
        alias="CORS_ORIGINS",
    )

    @property
    def allowed_origins(self) -> list[str]:
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
