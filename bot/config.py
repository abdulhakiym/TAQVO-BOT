
"""TAQVO PRO MAX — bot konfiguratsiyasi.
Python 3.11+ | Faqat standart Python kutubxonalari.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


def _int_env(
    name: str,
    default: int,
    *,
    minimum: int,
    maximum: int,
) -> int:
    raw = _env(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(
            f"{name} butun son bo‘lishi kerak: {raw!r}"
        ) from exc

    if not minimum <= value <= maximum:
        raise ValueError(
            f"{name} qiymati {minimum} va {maximum} oralig‘ida bo‘lishi kerak."
        )
    return value


def _admin_ids() -> tuple[int, ...]:
    raw = _env("ADMIN_IDS", "")
    if not raw:
        return ()

    try:
        ids = tuple(dict.fromkeys(
            int(item.strip())
            for item in raw.split(",")
            if item.strip()
        ))
    except ValueError as exc:
        raise ValueError(
            "ADMIN_IDS vergul bilan ajratilgan Telegram IDlar bo‘lishi kerak."
        ) from exc

    if any(user_id <= 0 for user_id in ids):
        raise ValueError("ADMIN_IDS ichidagi IDlar musbat son bo‘lishi kerak.")
    return ids


@dataclass(frozen=True, slots=True)
class Settings:
    bot_token: str
    channel_username: str
    channel_url: str
    mini_app_url: str

    database_path: Path

    default_city: str
    default_country: str
    prayer_method: int
    timezone: str

    port: int
    log_level: str
    admin_ids: tuple[int, ...]

    morning_reminder: str
    evening_reminder: str
    http_timeout_seconds: int
    telegram_init_data_max_age: int

    @classmethod
    def from_env(cls) -> "Settings":
        database_path = Path(
            _env("DATABASE_PATH", "data/taqvo.sqlite3")
        ).expanduser()

        channel_username = _env(
            "CHANNEL_USERNAME", "@hakiymqalb"
        )

        if channel_username and not (
            channel_username.startswith("@")
            or channel_username.startswith("-100")
        ):
            raise ValueError(
                "CHANNEL_USERNAME @kanal_nomi yoki -100... formatida bo‘lishi kerak."
            )

        channel_url = _env(
            "CHANNEL_URL", "https://t.me/hakiymqalb"
        )
        mini_app_url = _env(
            "SITE_URL",
            "https://abdulhakiym.github.io/TAQVO-BOT/",
        )

        if channel_url and not channel_url.startswith("https://"):
            raise ValueError("CHANNEL_URL https:// bilan boshlanishi kerak.")

        if mini_app_url and not mini_app_url.startswith("https://"):
            raise ValueError("SITE_URL https:// bilan boshlanishi kerak.")

        log_level = _env("LOG_LEVEL", "INFO").upper()

        if log_level not in {
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        }:
            raise ValueError("LOG_LEVEL noto‘g‘ri.")

        morning = _env("MORNING_REMINDER", "08:00")
        evening = _env("EVENING_REMINDER", "20:00")

        for variable, clock in (
            ("MORNING_REMINDER", morning),
            ("EVENING_REMINDER", evening),
        ):
            try:
                hour_text, minute_text = clock.split(":", maxsplit=1)
                hour, minute = int(hour_text), int(minute_text)
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"{variable} HH:MM formatida bo‘lishi kerak."
                ) from exc

            if not (
                0 <= hour <= 23 and 0 <= minute <= 59
            ):
                raise ValueError(
                    f"{variable} noto‘g‘ri vaqt: {clock!r}"
                )

        return cls(
            bot_token=_env("BOT_TOKEN", ""),
            channel_username=channel_username,
            channel_url=channel_url,
            mini_app_url=mini_app_url,
            database_path=database_path,
            default_city=_env("DEFAULT_CITY", "Karaganda"),
            default_country=_env("DEFAULT_COUNTRY", "Kazakhstan"),
            prayer_method=_int_env(
                "PRAYER_METHOD", 3, minimum=0, maximum=23
            ),
            timezone=_env("DEFAULT_TIMEZONE", "Asia/Almaty"),
            port=_int_env(
                "PORT", 10000, minimum=1, maximum=65535
            ),
            log_level=log_level,
            admin_ids=_admin_ids(),
            morning_reminder=morning,
            evening_reminder=evening,
            http_timeout_seconds=_int_env(
                "HTTP_TIMEOUT_SECONDS", 20, minimum=3, maximum=120
            ),
            telegram_init_data_max_age=_int_env(
                "TELEGRAM_INIT_DATA_MAX_AGE",
                86400,
                minimum=60,
                maximum=604800,
            ),
        )

    def validate_runtime(self) -> None:
        if not self.bot_token:
            raise RuntimeError(
                "BOT_TOKEN topilmadi. Render → Environment bo‘limiga "
                "BotFather tokenini kiriting."
            )

        if ":" not in self.bot_token:
            raise RuntimeError(
                "BOT_TOKEN formati noto‘g‘ri. BotFather tokenini tekshiring."
            )

        if not self.channel_username:
            raise RuntimeError(
                "CHANNEL_USERNAME bo‘sh bo‘lmasligi kerak."
            )


# Boshqa fayllarda: from config import settings
settings = Settings.from_env()
