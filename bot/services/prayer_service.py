
from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from html import escape
from typing import Optional
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import aiohttp

from config import settings


API_URL = "https://api.aladhan.com/v1/timingsByCity"


class PrayerServiceError(Exception):
    """Namoz vaqtlarini olishdagi xatolik."""


@dataclass(frozen=True)
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


def _valid_timezone(timezone_name: Optional[str]) -> str:
    for candidate in (timezone_name, settings.timezone, "UTC"):
        if not candidate:
            continue
        try:
            ZoneInfo(candidate)
            return candidate
        except (ZoneInfoNotFoundError, ValueError):
            continue
    return "UTC"


def _local_date(timezone_name: str) -> date:
    return datetime.now(ZoneInfo(timezone_name)).date()


def _clean_time(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise PrayerServiceError(f"{field_name} vaqti topilmadi.")

    match = re.search(r"(\d{1,2}):(\d{2})", value)
    if not match:
        raise PrayerServiceError(f"{field_name} vaqti noto‘g‘ri.")

    hour, minute = map(int, match.groups())
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise PrayerServiceError(f"{field_name} vaqti noto‘g‘ri.")

    return f"{hour:02d}:{minute:02d}"


def _validate_method(method: Optional[int]) -> int:
    selected = settings.prayer_method if method is None else method

    try:
        selected = int(selected)
    except (TypeError, ValueError):
        raise PrayerServiceError("Hisoblash usuli raqam bo‘lishi kerak.")

    if not 0 <= selected <= 23:
        raise PrayerServiceError("Hisoblash usuli 0–23 oralig‘ida bo‘lishi kerak.")

    return selected


async def fetch_prayer_times(
    session: aiohttp.ClientSession,
    city: str,
    country: str,
    method: Optional[int] = None,
    timezone_name: Optional[str] = None,
    target_date: Optional[date] = None,
) -> PrayerTimes:
    city = city.strip() if isinstance(city, str) else ""
    country = country.strip() if isinstance(country, str) else ""

    if not city or not country:
        raise PrayerServiceError("Shahar va davlat nomi kiritilishi kerak.")

    selected_method = _validate_method(method)
    selected_timezone = _valid_timezone(timezone_name)
    requested_date = target_date or _local_date(selected_timezone)
    api_date = requested_date.strftime("%d-%m-%Y")

    params = {
        "city": city,
        "country": country,
        "method": selected_method,
    }

    timeout = aiohttp.ClientTimeout(
        total=settings.http_timeout_seconds
    )

    try:
        async with session.get(
            f"{API_URL}/{api_date}",
            params=params,
            timeout=timeout,
        ) as response:
            if response.status != 200:
                raise PrayerServiceError(
                    f"Namoz API xatoligi: HTTP {response.status}"
                )

            try:
                payload = await response.json()
            except (ValueError, aiohttp.ContentTypeError):
                raise PrayerServiceError("Namoz API noto‘g‘ri javob qaytardi.")

    except asyncio.TimeoutError:
        raise PrayerServiceError("So‘rov vaqti tugadi. Keyinroq urinib ko‘ring.")
    except aiohttp.ClientError:
        raise PrayerServiceError("Namoz API bilan bog‘lanib bo‘lmadi.")

    if not isinstance(payload, dict) or payload.get("code") != 200:
        raise PrayerServiceError("Namoz vaqtlari olinmadi.")

    data = payload.get("data")
    if not isinstance(data, dict):
        raise PrayerServiceError("API javobida ma’lumot topilmadi.")

    timings = data.get("timings")
    if not isinstance(timings, dict):
        raise PrayerServiceError("Namoz vaqtlari topilmadi.")

    meta = data.get("meta") or {}
    api_timezone = meta.get("timezone")

    if isinstance(api_timezone, str):
        selected_timezone = _valid_timezone(api_timezone)

    method_info = meta.get("method") or {}
    method_name = (
        method_info.get("name")
        if isinstance(method_info, dict)
        else None
    )
    if not isinstance(method_name, str) or not method_name.strip():
        method_name = f"Hisoblash usuli {selected_method}"

    return PrayerTimes(
        city=city,
        country=country,
        date=requested_date.strftime("%d.%m.%Y"),
        timezone=selected_timezone,
        calculation_method=method_name,
        fajr=_clean_time(timings.get("Fajr"), "Bomdod"),
        sunrise=_clean_time(timings.get("Sunrise"), "Quyosh chiqishi"),
        dhuhr=_clean_time(timings.get("Dhuhr"), "Peshin"),
        asr=_clean_time(timings.get("Asr"), "Asr"),
        maghrib=_clean_time(timings.get("Maghrib"), "Shom"),
        isha=_clean_time(timings.get("Isha"), "Xufton"),
    )


def format_prayer_message(prayer: PrayerTimes) -> str:
    return (
        "🕌 <b>NAMOZ VAQTLARI</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📍 <b>{escape(prayer.city)}, {escape(prayer.country)}</b>\n"
        f"📅 Sana: <b>{escape(prayer.date)}</b>\n"
        f"🌍 Vaqt zonasi: <code>{escape(prayer.timezone)}</code>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🌅 Bomdod: <b>{prayer.fajr}</b>\n"
        f"☀️ Quyosh chiqishi: <b>{prayer.sunrise}</b>\n"
        f"🌤 Peshin: <b>{prayer.dhuhr}</b>\n"
        f"🌇 Asr: <b>{prayer.asr}</b>\n"
        f"🌆 Shom: <b>{prayer.maghrib}</b>\n"
        f"🌙 Xufton: <b>{prayer.isha}</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📖 Hisoblash usuli: <i>{escape(prayer.calculation_method)}</i>\n\n"
        "Alloh taolo namozlaringizni qabul qilsin."
    )
