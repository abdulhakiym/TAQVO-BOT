import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str

    CHANNEL_USERNAME: str = "@hakiymqalb"

    MINI_APP_URL: str = ""

    TIMEZONE: str = "UTC"

    ADMIN_IDS: str = ""

    WEBHOOK_URL: str = ""
    WEBHOOK_SECRET: str = ""

    PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @property
    def admin_id_list(self) -> list[int]:
        result = []

        for value in self.ADMIN_IDS.split(","):
            value = value.strip()

            if value.isdigit():
                result.append(int(value))

        return result


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
