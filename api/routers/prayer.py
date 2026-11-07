"""Worldwide city search and prayer times for TAQVO PRO MAX."""

from datetime import datetime, timezone
from time import monotonic
from typing import Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx
from fastapi import APIRouter, HTTPException, Query


router = APIRouter(
    prefix="/api/prayer",
    tags=["Prayer Times"],
)

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
ALADHAN_URL = "https://api.aladhan.com/v1"

REQUEST_TIMEOUT = 15.0
CACHE_SECONDS = 300

_prayer_cache: dict[str, tuple[float, dict[str, Any]]] = {}

Madhhab = Literal["hanafi", "maliki", "shafii", "hanbali"]

MADHHAB_NAMES = {
    "hanafi": "Hanafi",
    "maliki": "Maliki",
    "shafii": "Shafi'i",
    "hanbali": "Hanbali",
}


def _clean_time(value: str | None) -> str | None:
    if not value:
        return None

    return value.split(" ")[0].strip()


@router.get("/cities")
async def search_cities(
    q: str = Query(min_length=2, max_length=100),
    count: int = Query(default=10, ge=1, le=20),
    language: str = Query(default="en", min_length=2, max_length=5),
) -> dict[str, Any]:

    query = q.strip()

    if len(query) < 2:
        raise HTTPException(
            status_code=422,
            detail="Shahar nomini kamida 2 ta harf bilan kiriting.",
        )

    params = {
        "name": query,
        "count": count,
        "language": language,
        "format": "json",
    }

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT
        ) as client:
            response = await client.get(
                GEOCODING_URL,
                params=params,
            )
            response.raise_for_status()
            payload = response.json()

    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="Shahar qidirish xizmati vaqtida javob bermadi.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Shahar qidirish xizmatida xatolik yuz berdi.",
        ) from exc

    cities = []

    for item in payload.get("results", []):
        latitude = item.get("latitude")
        longitude = item.get("longitude")
        city_timezone = item.get("timezone")

        if (
            latitude is None
            or longitude is None
            or not city_timezone
        ):
            continue

        cities.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "country": item.get("country"),
            "country_code": item.get("country_code"),
            "region": item.get("admin1"),
            "latitude": latitude,
            "longitude": longitude,
            "timezone": city_timezone,
        })

    return {
        "success": True,
        "count": len(cities),
        "results": cities,
    }


@router.get("/today")
async def get_today_prayer_times(
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    timezone_name: str = Query(
        alias="timezone",
        min_length=1,
        max_length=64,
    ),
    method: int = Query(default=3),
    madhhab: Madhhab = Query(default="hanafi"),
    school: int | None = Query(default=None, ge=0, le=1),
) -> dict[str, Any]:
    """
    Get today's prayer times for a worldwide location.

    Hanafi uses the Hanafi Asr calculation.
    Maliki, Shafi'i and Hanbali use the standard Asr calculation.
    """

    if method not in {*range(0, 24), 99}:
        raise HTTPException(
            status_code=422,
            detail="Namoz hisoblash usuli noto'g'ri.",
        )

    try:
        city_timezone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail="Vaqt zonasi noto'g'ri yoki topilmadi.",
        ) from exc

    # AlAdhan supports two Asr calculation schools:
    # 1 = Hanafi, 0 = standard.
    # Keep the old 'school' parameter for compatibility.
    if school is not None:
        asr_school = school
        selected_madhhab = (
            "hanafi" if school == 1 else madhhab
        )
    else:
        selected_madhhab = madhhab
        asr_school = 1 if madhhab == "hanafi" else 0

    local_date = datetime.now(city_timezone).date()
    date_string = local_date.strftime("%d-%m-%Y")

    cache_key = (
        f"{latitude:.5f}:{longitude:.5f}:"
        f"{timezone_name}:{method}:{asr_school}:"
        f"{selected_madhhab}:{date_string}"
    )

    cached = _prayer_cache.get(cache_key)

    if cached and monotonic() - cached[0] < CACHE_SECONDS:
        return cached[1]

    endpoint = f"{ALADHAN_URL}/timings/{date_string}"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "method": method,
        "school": asr_school,
        "timezonestring": timezone_name,
    }

    try:
        async with httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT
        ) as client:
            response = await client.get(
                endpoint,
                params=params,
            )
            response.raise_for_status()
            payload = response.json()

    except httpx.TimeoutException as exc:
        raise HTTPException(
            status_code=504,
            detail="Namoz vaqtlari xizmati vaqtida javob bermadi.",
        ) from exc

    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Namoz vaqtlari xizmatida xatolik yuz berdi.",
        ) from exc

    if payload.get("code") != 200:
        raise HTTPException(
            status_code=502,
            detail="Namoz vaqtlari API to'g'ri ma'lumot qaytarmadi.",
        )

    data = payload.get("data", {})
    raw_timings = data.get("timings", {})

    required_times = {
        "fajr": raw_timings.get("Fajr"),
        "dhuhr": raw_timings.get("Dhuhr"),
        "asr": raw_timings.get("Asr"),
        "maghrib": raw_timings.get("Maghrib"),
        "isha": raw_timings.get("Isha"),
    }

    if not all(required_times.values()):
        raise HTTPException(
            status_code=502,
            detail="Namoz vaqtlarining ayrimlari mavjud emas.",
        )

    result = {
        "success": True,
        "date": local_date.isoformat(),
        "timezone": timezone_name,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "timings": {
            key: _clean_time(value)
            for key, value in required_times.items()
        },
        "sunrise": _clean_time(raw_timings.get("Sunrise")),
        "hijri": data.get("date", {}).get("hijri", {}),
        "meta": {
            "calculation_method": data.get(
                "meta", {}
            ).get("method", {}),
            "madhhab": selected_madhhab,
            "madhhab_name": MADHHAB_NAMES[selected_madhhab],
            "asr_school": (
                "hanafi" if asr_school == 1 else "standard"
            ),
            "source": "AlAdhan Prayer Times API",
            "updated_at": datetime.now(
                timezone.utc
            ).isoformat(),
        },
    }

    _prayer_cache[cache_key] = (monotonic(), result)

    return result
