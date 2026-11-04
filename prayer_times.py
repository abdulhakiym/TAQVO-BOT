from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx


GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)

PRAYER_API_URL = (
    "https://api.aladhan.com/v1/timings"
)

PRAYER_NAMES = {
    "Fajr": "Bomdod",
    "Dhuhr": "Peshin",
    "Asr": "Asr",
    "Maghrib": "Shom",
    "Isha": "Xufton",
}


class PrayerTimesError(Exception):
    """Namoz vaqtlarini olishdagi xatolik."""


async def search_cities(
    query: str,
    limit: int = 10,
) -> list[dict]:
    """Dunyo bo‘yicha shaharlarni nomi orqali qidirish."""

    query = query.strip()

    if len(query) < 2:
        return []

    limit = max(1, min(limit, 20))

    params = {
        "name": query,
        "count": limit,
        "language": "en",
        "format": "json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=15.0
        ) as client:
            response = await client.get(
                GEOCODING_URL,
                params=params,
            )
            response.raise_for_status()
            data = response.json()

    except (httpx.HTTPError, ValueError) as exc:
        raise PrayerTimesError(
            "Shaharlarni qidirish xizmati vaqtincha ishlamayapti."
        ) from exc

    results = []

    for item in data.get("results", []):
        latitude = item.get("latitude")
        longitude = item.get("longitude")
        timezone = item.get("timezone")

        if (
            latitude is None
            or longitude is None
            or not timezone
        ):
            continue

        try:
            ZoneInfo(timezone)
        except (ZoneInfoNotFoundError, ValueError):
            continue

        results.append({
            "id": str(item.get("id", "")),
            "name": item.get("name", ""),
            "country": item.get("country", ""),
            "country_code": item.get("country_code", ""),
            "latitude": float(latitude),
            "longitude": float(longitude),
            "timezone": timezone,
            "admin1": item.get("admin1", ""),
        })

    return results


async def get_prayer_times(
    latitude: float,
    longitude: float,
    timezone: str,
    method: int = 3,
    school: int = 1,
) -> dict:
    """
    Tanlangan koordinatalar uchun namoz vaqtlarini oladi.

    method=3: Muslim World League.
    school=1: Hanafi Asr.
    school=0: Shafi'i, Maliki va Hanbali Asr.
    """

    if not -90 <= latitude <= 90:
        raise ValueError("Noto‘g‘ri latitude")

    if not -180 <= longitude <= 180:
        raise ValueError("Noto‘g‘ri longitude")

    if school not in (0, 1):
        raise ValueError("Noto‘g‘ri Asr hisoblash usuli")

    try:
        local_date = datetime.now(
            ZoneInfo(timezone)
        )
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(
            "Noto‘g‘ri vaqt zonasi"
        ) from exc

    date_path = local_date.strftime("%d-%m-%Y")

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "method": method,
        "school": school,
        "timezonestring": timezone,
    }

    try:
        async with httpx.AsyncClient(
            timeout=20.0
        ) as client:
            response = await client.get(
                f"{PRAYER_API_URL}/{date_path}",
                params=params,
            )
            response.raise_for_status()
            payload = response.json()

    except (httpx.HTTPError, ValueError) as exc:
        raise PrayerTimesError(
            "Namoz vaqtlarini olish imkoni bo‘lmadi."
        ) from exc

    if payload.get("code") != 200:
        raise PrayerTimesError(
            "Namoz vaqtlari API xatosi."
        )

    data = payload.get("data", {})
    timings = data.get("timings", {})

    result = {}

    for api_name, uzbek_name in PRAYER_NAMES.items():
        value = timings.get(api_name)

        if not value:
            raise PrayerTimesError(
                f"{uzbek_name} vaqti topilmadi."
            )

        result[uzbek_name] = value.split(" ")[0]

    result["date"] = local_date.strftime("%Y-%m-%d")
    result["timezone"] = timezone
    result["method"] = method
    result["school"] = school

    return result


def format_prayer_times(
    city: str,
    times: dict,
) -> str:
    """Namoz vaqtlarini Telegram uchun chiroyli formatlaydi."""

    return (
        f"🕌 NAMOZ VAQTLARI\n"
        f"📍 Shahar: {city}\n"
        f"📅 Sana: {times['date']}\n\n"
        f"🌅 Bomdod: {times['Bomdod']}\n"
        f"☀️ Peshin: {times['Peshin']}\n"
        f"🌤 Asr: {times['Asr']}\n"
        f"🌇 Shom: {times['Shom']}\n"
        f"🌙 Xufton: {times['Xufton']}\n\n"
        f"🕰 Vaqt zonasi: {times['timezone']}"
    )
