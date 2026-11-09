"""TAQVO BOT prayer time service."""

import asyncio
import json
import logging

from datetime import date, datetime
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from bot.config import get_settings


logger = logging.getLogger(__name__)

PRAYER_NAMES = (
    "Fajr",
    "Sunrise",
    "Dhuhr",
    "Asr",
    "Maghrib",
    "Isha",
)


class PrayerAPIError(Exception):
    """Prayer API request or response error."""


def _fetch_prayer_times(
    city: str,
    country: str,
    target_date: str,
    method: int,
    school: int,
) -> dict[str, Any]:
    """Fetch prayer timings from Aladhan API."""

    settings = get_settings()

    base_url = settings.prayer_api_base_url.rstrip("/")
    endpoint = f"{base_url}/timingsByCity/{target_date}"

    params = urlencode({
        "city": city,
        "country": country,
        "method": method,
        "school": school,
    })

    request = Request(
        f"{endpoint}?{params}",
        headers={
            "User-Agent": "TAQVO-BOT/1.0",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(
                response.read().decode("utf-8")
            )
    except Exception as exc:
        raise PrayerAPIError(
            "Namoz vaqtlarini olishda API xatosi."
        ) from exc

    if payload.get("code") != 200:
        raise PrayerAPIError(
            "Aladhan API muvaffaqiyatli javob qaytarmadi."
        )

    data = payload.get("data")

    if not isinstance(data, dict):
        raise PrayerAPIError(
            "API javobida ma'lumot topilmadi."
        )

    timings = data.get("timings", {})

    result = {}

    for name in PRAYER_NAMES:
        value = timings.get(name)

        if not value:
            raise PrayerAPIError(
                f"{name} vaqti API javobida mavjud emas."
            )

        result[name] = str(value).split(" ")[0]

    return {
        "city": city,
        "country": country,
        "date": target_date,
        "timezone": data.get("meta", {}).get("timezone"),
        "timings": result,
        "method": method,
        "school": school,
    }


async def get_prayer_times(
    city: str,
    country: str,
    target_date: date | None = None,
    timezone: str | None = None,
    method: int | None = None,
    school: int | None = None,
) -> dict[str, Any]:
    """Get prayer times for a selected city and date."""

    city = city.strip()
    country = country.strip()

    if not city or not country:
        raise ValueError(
            "Shahar va davlat nomi kiritilishi kerak."
        )

    settings = get_settings()

    timezone_name = (
        timezone or settings.default_timezone
    )

    if target_date is None:
        try:
            target_date = datetime.now(
                ZoneInfo(timezone_name)
            ).date()
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise ValueError(
                f"Noto'g'ri vaqt mintaqasi: {timezone_name}"
            ) from exc

    selected_method = (
        settings.prayer_calculation_method
        if method is None
        else method
    )

    selected_school = (
        settings.prayer_asr_method
        if school is None
        else school
    )

    if selected_method < 0:
        raise ValueError(
            "Namoz hisoblash usuli noto'g'ri."
        )

    if selected_school not in (0, 1):
        raise ValueError(
            "Asr hisoblash usuli 0 yoki 1 bo'lishi kerak."
        )

    date_string = target_date.strftime("%d-%m-%Y")

    try:
        return await asyncio.to_thread(
            _fetch_prayer_times,
            city,
            country,
            date_string,
            selected_method,
            selected_school,
        )
    except PrayerAPIError:
        logger.exception(
            "Prayer API error: %s, %s",
            city,
            country,
        )
        raise


async def get_today_prayer_times(
    city: str,
    country: str,
    timezone: str | None = None,
) -> dict[str, Any]:
    """Get today's prayer times."""

    return await get_prayer_times(
        city=city,
        country=country,
        timezone=timezone,
    )
