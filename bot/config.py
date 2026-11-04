"""
TAQVO PRO MAX — bot konfiguratsiyasi.
Python 3.11+
Faqat standart Python kutubxonalari.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def _env_alias(
    primary: str,
    secondary: str,
    default: str,
) -> str:
    """Eski va yangi environment nomlarini qo‘llab-quvvatlaydi."""
    return _env(primary) or _env(secondary) or default


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
    raw = _env("ADMIN_IDS")

    if not raw:
        return ()

    try:
        ids = tuple(
            dict.fromkeys(
                int(item.strip())
                for item in raw.split(",")
                if item.strip()
            )
        )
    except ValueError as exc:
        raise ValueError(
            "ADMIN_IDS vergul bilan ajratilgan Telegram IDlar bo‘lishi kerak."
        ) from exc

    if any(user_id <= 0 for user_id in ids):
        raise ValueError(
            "ADMIN_IDS ichidagi IDlar musbat son bo‘lishi kerak."
        )

    return ids


def _validate_url(name: str, value: str) -> None:
    """HTTPS URL formatini tekshiradi."""
    if not value:
        raise ValueError(f"{name} bo‘sh bo‘lmasligi kerak.")

    parsed = urlparse(value)

    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError(
            f"{name} to‘g‘ri HTTPS manzil bo‘lishi kerak."
        )


def _validate_clock(name: str, value: str) -> str:
    """HH:MM formatidagi vaqtni tekshiradi."""
    try:
        hour_text, minute_text = value.split(":")
        hour = int(hour_text)
        minute = int(minute_text)
    except (ValueError, TypeError):
        raise ValueError(
            f"{name} HH:MM formatida bo‘lishi kerak."
        )

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(
            f"{name} noto‘g‘ri vaqt: {value!r}"
        )

    return f"{hour:02d}:{minute:02d}"


def _validate_timezone(value: str) -> str:
    """IANA vaqt zonasini tekshiradi."""
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError(
            f"TIMEZONE noto‘g‘ri: {value!r}"
        )

    return value


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
        """Environment Variables orqali sozlamalarni yuklaydi."""

        database_path = Path(
            _env(
                "DATABASE_PATH",
                "data/taqvo.sqlite3",
            )
        ).expanduser()

        channel_username = _env(
            "CHANNEL_USERNAME",
            "@hakiymqalb",
        )

        if not channel_username.startswith("@") and not channel_username.startswith("-100"):
            raise ValueError(
                "CHANNEL_USERNAME @kanal_nomi yoki -100... formatida bo‘lishi kerak."
            )

        channel_url = _env(
            "CHANNEL_URL",
            "https://t.me/hakiymqalb",
        )

        mini_app_url = _env_alias(
            "SITE_URL",
            "MINI_APP_URL",
            "https://abdulhakiym.github.io/TAQVO-BOT/",
        )

        _validate_url("CHANNEL_URL", channel_url)
        _validate_url("SITE_URL", mini_app_url)

        log_level = _env(
            "LOG_LEVEL",
            "INFO",
        ).upper()

        allowed_log_levels = {
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        }

        if log_level not in allowed_log_levels:
            raise ValueError("LOG_LEVEL noto‘g‘ri.")

        morning = _validate_clock(
            "REMINDER_MORNING",
            _env("REMINDER_MORNING", "08:00"),
        )

        evening = _validate_clock(
            "REMINDER_EVENING",
            _env("REMINDER_EVENING", "20:00"),
        )

        timezone_name = _validate_timezone(
            _env_alias(
                "TIMEZONE",
                "DEFAULT_TIMEZONE",
                "Asia/Almaty",
            )
        )

        return cls(
            bot_token=_env("BOT_TOKEN"),

            channel_username=channel_username,
            channel_url=channel_url,

            mini_app_url=mini_app_url,

            database_path=database_path,

            default_city=_env(
                "DEFAULT_CITY",
                "Karaganda",
            ),

            default_country=_env(
                "DEFAULT_COUNTRY",
                "Kazakhstan",
            ),

            prayer_method=_int_env(
                "PRAYER_METHOD",
                3,
                minimum=0,
                maximum=23,
            ),

            timezone=timezone_name,

            port=_int_env(
                "PORT",
                10000,
                minimum=1,
                maximum=65535,
            ),

            log_level=log_level,

            admin_ids=_admin_ids(),

            morning_reminder=morning,
            evening_reminder=evening,

            http_timeout_seconds=_int_env(
                "HTTP_TIMEOUT_SECONDS",
                20,
                minimum=3,
                maximum=120,
            ),

            telegram_init_data_max_age=_int_env(
                "TELEGRAM_INIT_DATA_MAX_AGE",
                86400,
                minimum=60,
                maximum=604800,
            ),
        )

    def validate_runtime(self) -> None:
        """Bot ishga tushishidan oldin muhim sozlamalarni tekshiradi."""

        if not self.bot_token:
            raise RuntimeError(
                "BOT_TOKEN topilmadi. "
                "Render → Environment bo‘limiga "
                "BotFather tokenini kiriting."
            )

        if ":" not in self.bot_token:
            raise RuntimeError(
                "BOT_TOKEN formati noto‘g‘ri. "
                "BotFather tokenini tekshiring."
            )

        if not self.channel_username:
            raise RuntimeError(
                "CHANNEL_USERNAME bo‘sh bo‘lmasligi kerak."
            )


# Boshqa fayllarda: from config import settings
settings = Settings.from_env()
