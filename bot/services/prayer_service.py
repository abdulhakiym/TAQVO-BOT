"""
TAQVO PRO MAX — Namoz vaqtlarini hisoblash xizmati.
Python 3.11+
AlAdhan API
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass
from datetime import date, datetime
from html import escape
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import aiohttp

from config import settings


logger = logging.getLogger(__name__)

API_URL = "https://api.aladhan.com/v1/timingsByCity"


class PrayerServiceError(Exception):
    """Namoz vaqtlarini olishdagi xatolik."""


@dataclass(frozen=True, slots=True)
class PrayerTimes:
    city: str
    country: str
    date: str
    timezone: str
    calculation_method: str
    fajr: str
    sunrise: str
    dhuhr: str
    asr: str
    maghrib: str
    isha: str


# =========================================================
# YORDAMCHI FUNKSIYALAR
# =========================================================

def _valid_timezone(timezone_name: str | None) -> str:
    """Berilgan vaqt zonasini tekshiradi."""

    candidates = (
        timezone_name,
        settings.timezone,
        "UTC",
    )

    for candidate in candidates:
        if not isinstance(candidate, str) or not candidate.strip():
            continue

        try:
            ZoneInfo(candidate)
            return candidate

        except (ZoneInfoNotFoundError, ValueError):
            continue

    return "UTC"


def _local_date(timezone_name: str) -> date:
    """Tanlangan vaqt zonasi bo‘yicha bugungi sanani qaytaradi."""

    return datetime.now(
        ZoneInfo(timezone_name)
    ).date()


def _clean_time(
    value: object,
    field_name: str,
) -> str:
    """API qaytargan namoz vaqtini HH:MM formatiga keltiradi."""

    if not isinstance(value, str):
        raise PrayerServiceError(
            f"{field_name} vaqti API javobida topilmadi."
        )

    match = re.search(
        r"^\s*(\d{1,2}):(\d{2})",
        value,
    )

    if not match:
        raise PrayerServiceError(
            f"{field_name} vaqti noto‘g‘ri."
        )

    hour, minute = map(int, match.groups())

    if not (
        0 <= hour <= 23
        and 0 <= minute <= 59
    ):
        raise PrayerServiceError(
            f"{field_name} vaqti noto‘g‘ri."
        )

    return f"{hour:02d}:{minute:02d}"


def _validate_method(method: int | None) -> int:
    """Namoz hisoblash usulini tekshiradi."""

    selected = (
        settings.prayer_method
        if method is None
        else method
    )

    if isinstance(selected, bool):
        raise PrayerServiceError(
            "Hisoblash usuli noto‘g‘ri."
        )

    try:
        selected = int(selected)

    except (TypeError, ValueError) as exc:
        raise PrayerServiceError(
            "Hisoblash usuli raqam bo‘lishi kerak."
        ) from exc

    if not 0 <= selected <= 23:
        raise PrayerServiceError(
            "Hisoblash usuli 0–23 oralig‘ida bo‘lishi kerak."
        )

    return selected


def _api_timezone(
    meta: dict,
    fallback: str,
) -> str:
    """API qaytargan vaqt zonasini tekshiradi."""

    timezone_name = meta.get("timezone")

    if isinstance(timezone_name, str) and timezone_name.strip():
        try:
            ZoneInfo(timezone_name)
            return timezone_name

        except (ZoneInfoNotFoundError, ValueError):
            logger.warning(
                "AlAdhan noto‘g‘ri vaqt zonasi qaytardi: %s",
                timezone_name,
            )

    return fallback


# =========================================================
# NAMOZ VAQTLARINI OLISH
# =========================================================

async def fetch_prayer_times(
    session: aiohttp.ClientSession,
    city: str,
    country: str,
    method: int | None = None,
    timezone_name: str | None = None,
    target_date: date | None = None,
) -> PrayerTimes:
    """
    AlAdhan API orqali namoz vaqtlarini oladi.

    session:
        aiohttp ClientSession

    city:
        Foydalanuvchining shahri

    country:
        Foydalanuvchining davlati

    method:
        AlAdhan hisoblash usuli

    timezone_name:
        Foydalanuvchining IANA vaqt zonasi

    target_date:
        Hisoblanadigan sana
    """

    # Shahar va davlatni tekshirish.
    city = city.strip() if isinstance(city, str) else ""
    country = country.strip() if isinstance(country, str) else ""

    if not city or not country:
        raise PrayerServiceError(
            "Shahar va davlat nomi kiritilishi kerak."
        )

    if len(city) > 100 or len(country) > 100:
        raise PrayerServiceError(
            "Shahar yoki davlat nomi juda uzun."
        )

    # Hisoblash usuli.
    selected_method = _validate_method(method)

    # Foydalanuvchining vaqt zonasi.
    selected_timezone = _valid_timezone(timezone_name)

    # Sana.
    if target_date is not None and not isinstance(target_date, date):
        raise PrayerServiceError(
            "Hisoblanadigan sana noto‘g‘ri."
        )

    requested_date = (
        target_date
        if target_date is not None
        else _local_date(selected_timezone)
    )

    api_date = requested_date.strftime("%d-%m-%Y")

    params = {
        "city": city,
        "country": country,
        "method": selected_method,
    }

    timeout = aiohttp.ClientTimeout(
        total=settings.http_timeout_seconds
    )

    url = f"{API_URL}/{api_date}"

    # API so‘rovi.
    try:
        async with session.get(
            url,
            params=params,
            timeout=timeout,
        ) as response:

            if response.status != 200:
                logger.warning(
                    "AlAdhan API HTTP xatoligi: %s",
                    response.status,
                )

                raise PrayerServiceError(
                    "Namoz API bilan bog‘lanishda xatolik yuz berdi."
                )

            try:
                payload = await response.json()

            except (ValueError, aiohttp.ContentTypeError) as exc:
                raise PrayerServiceError(
                    "Namoz API noto‘g‘ri javob qaytardi."
                ) from exc

    except asyncio.TimeoutError as exc:
        logger.warning("AlAdhan API so‘rovi vaqti tugadi.")

        raise PrayerServiceError(
            "So‘rov vaqti tugadi. Keyinroq urinib ko‘ring."
        ) from exc

    except aiohttp.ClientError as exc:
        logger.exception("AlAdhan API bilan aloqa xatoligi.")

        raise PrayerServiceError(
            "Namoz API bilan bog‘lanib bo‘lmadi."
        ) from exc

    # API umumiy javobini tekshirish.
    if not isinstance(payload, dict):
        raise PrayerServiceError(
            "API javobining formati noto‘g‘ri."
        )

    if payload.get("code") != 200:
        logger.warning(
            "AlAdhan API xato javob qaytardi: %s",
            payload.get("status"),
        )

        raise PrayerServiceError(
            "Namoz vaqtlarini olish imkoni bo‘lmadi."
        )

    data = payload.get("data")

    if not isinstance(data, dict):
        raise PrayerServiceError(
            "API javobida ma’lumot topilmadi."
        )

    # Namoz vaqtlarini tekshirish.
    timings = data.get("timings")

    if not isinstance(timings, dict):
        raise PrayerServiceError(
            "Namoz vaqtlari topilmadi."
        )

    # API qaytargan vaqt zonasi.
    meta = data.get("meta")

    if not isinstance(meta, dict):
        meta = {}

    selected_timezone = _api_timezone(
        meta,
        selected_timezone,
    )

    # Hisoblash usuli nomi.
    method_info = meta.get("method")

    method_name = None

    if isinstance(method_info, dict):
        method_name = method_info.get("name")

    if not isinstance(method_name, str) or not method_name.strip():
        method_name = f"Hisoblash usuli {selected_method}"

    # Sana va namoz vaqtlarini qaytarish.
    return PrayerTimes(
        city=city,
        country=country,
        date=requested_date.strftime("%d.%m.%Y"),
        timezone=selected_timezone,
        calculation_method=method_name.strip(),

        fajr=_clean_time(
            timings.get("Fajr"),
            "Bomdod",
        ),

        sunrise=_clean_time(
            timings.get("Sunrise"),
            "Quyosh chiqishi",
        ),

        dhuhr=_clean_time(
            timings.get("Dhuhr"),
            "Peshin",
        ),

        asr=_clean_time(
            timings.get("Asr"),
            "Asr",
        ),

        maghrib=_clean_time(
            timings.get("Maghrib"),
            "Shom",
        ),

        isha=_clean_time(
            timings.get("Isha"),
            "Xufton",
        ),
    )


# =========================================================
# NAMOZ VAQTLARINI CHIROYLI FORMATLASH
# =========================================================

def format_prayer_message(
    prayer: PrayerTimes,
) -> str:
    """Namoz vaqtlarini Telegram HTML formatida chiqaradi."""

    city = escape(prayer.city)
    country = escape(prayer.country)
    prayer_date = escape(prayer.date)
    timezone_name = escape(prayer.timezone)
    method_name = escape(prayer.calculation_method)

    return (
        "🕌 <b>NAMOZ VAQTLARI</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📍 <b>{city}, {country}</b>\n"
        f"📅 Sana: <b>{prayer_date}</b>\n"
        f"🌍 Vaqt zonasi: <code>{timezone_name}</code>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🌅 Bomdod: <b>{prayer.fajr}</b>\n"
        f"☀️ Quyosh chiqishi: <b>{prayer.sunrise}</b>\n"
        f"🌤 Peshin: <b>{prayer.dhuhr}</b>\n"
        f"🌇 Asr: <b>{prayer.asr}</b>\n"
        f"🌆 Shom: <b>{prayer.maghrib}</b>\n"
        f"🌙 Xufton: <b>{prayer.isha}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📖 Hisoblash usuli: <i>{method_name}</i>\n\n"
        "Alloh taolo namozlaringizni qabul qilsin."
    )
