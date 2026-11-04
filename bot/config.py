"""
TAQVO PRO MAX — bot konfiguratsiyasi.
Python 3.11+
Faqat standart Python kutubxonalari.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def _env(name: str, default: str = "") -> str:
    """Environment qiymatini xavfsiz o‘qiydi."""
    return os.getenv(name, default).strip() or default


def _env_alias(
    primary: str,
    secondary: str,
    default: str,
) -> str:
    """Yangi va eski environment nomlarini qo‘llab-quvvatlaydi."""
    return (
        os.getenv(primary, "").strip()
        or os.getenv(secondary, "").strip()
        or default
    )


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
            f"{name} qiymati {minimum} va {maximum} "
            "oralig‘ida bo‘lishi kerak."
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


def _validate_url(name: str, value: str) -> str:
    """HTTPS URL formatini tekshiradi."""
    parsed = urlparse(value)

    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or any(char.isspace() for char in value)
    ):
        raise ValueError(
            f"{name} to‘g‘ri HTTPS manzil bo‘lishi kerak."
        )

    return value


def _validate_channel_username(value: str) -> str:
    """Telegram kanal username yoki ID formatini tekshiradi."""

    if value.startswith("@"):
        username = value[1:]

        if not re.fullmatch(r"[A-Za-z0-9_]{5,32}", username):
            raise ValueError(
                "CHANNEL_USERNAME noto‘g‘ri. "
                "Masalan: @hakiymqalb"
            )

        return value

    if re.fullmatch(r"-100\d+", value):
        return value

    raise ValueError(
        "CHANNEL_USERNAME @kanal_nomi yoki -100... "
        "formatida bo‘lishi kerak."
    )


def _validate_clock(name: str, value: str) -> str:
    """HH:MM formatidagi vaqtni tekshiradi."""

    if not re.fullmatch(r"\d{1,2}:\d{2}", value):
        raise ValueError(
            f"{name} HH:MM formatida bo‘lishi kerak."
        )

    hour_text, minute_text = value.split(":")
    hour = int(hour_text)
    minute = int(minute_text)

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(
            f"{name} noto‘g‘ri vaqt: {value!r}"
        )

    return f"{hour:02d}:{minute:02d}"


def _validate_timezone(value: str) -> str:
    """IANA vaqt zonasini tekshiradi."""

    if not value:
        raise ValueError("TIMEZONE bo‘sh bo‘lmasligi kerak.")

    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(
            f"TIMEZONE noto‘g‘ri yoki tizimda mavjud emas: {value!r}"
        ) from exc

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

        channel_username = _validate_channel_username(
            _env(
                "CHANNEL_USERNAME",
                "@hakiymqalb",
            )
        )

        channel_url = _validate_url(
            "CHANNEL_URL",
            _env(
                "CHANNEL_URL",
                "https://t.me/hakiymqalb",
            ),
        )

        mini_app_url = _validate_url(
            "SITE_URL",
            _env_alias(
                "SITE_URL",
                "MINI_APP_URL",
                "https://abdulhakiym.github.io/TAQVO-BOT/",
            ),
        )

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
            raise ValueError(
                f"LOG_LEVEL noto‘g‘ri: {log_level!r}"
            )

        morning = _validate_clock(
            "REMINDER_MORNING",
            _env_alias(
                "REMINDER_MORNING",
                "MORNING_REMINDER",
                "08:00",
            ),
        )

        evening = _validate_clock(
            "REMINDER_EVENING",
            _env_alias(
                "REMINDER_EVENING",
                "EVENING_REMINDER",
                "20:00",
            ),
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

        if not re.fullmatch(r"\d+:[A-Za-z0-9_-]+", self.bot_token):
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
