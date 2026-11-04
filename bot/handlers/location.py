from __future__ import annotations

import logging
from html import escape
from math import isfinite
from typing import Any

import aiohttp
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import settings
from database import set_location
from keyboards import main_keyboard, mini_app_keyboard


logger = logging.getLogger(__name__)

router = Router(name="location")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"
TIMEZONE_URL = "https://api.open-meteo.com/v1/forecast"

CITY_RESULTS: dict[int, list[dict[str, Any]]] = {}

RESERVED_TEXTS = {
    "🕌 Namoz vaqtlarim",
    "❌ Bekor qilish",
}


def _timeout() -> aiohttp.ClientTimeout:
    return aiohttp.ClientTimeout(
        total=settings.http_timeout_seconds,
    )


def _valid_coordinates(
    latitude: float,
    longitude: float,
) -> bool:
    return (
        isfinite(latitude)
        and isfinite(longitude)
        and -90 <= latitude <= 90
        and -180 <= longitude <= 180
    )


def _valid_timezone(timezone_name: object) -> bool:
    if not isinstance(timezone_name, str):
        return False

    if not timezone_name.strip():
        return False

    from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

    try:
        ZoneInfo(timezone_name)
        return True
    except (ZoneInfoNotFoundError, ValueError):
        return False


async def search_cities(
    session: aiohttp.ClientSession,
    query: str,
) -> list[dict[str, Any]]:
    params = {
        "name": query,
        "count": 8,
        "language": "en",
        "format": "json",
    }

    try:
        async with session.get(
            GEOCODING_URL,
            params=params,
            timeout=_timeout(),
        ) as response:
            if response.status != 200:
                logger.warning(
                    "Geocoding API HTTP status: %s",
                    response.status,
                )
                return []

            payload = await response.json()

    except (aiohttp.ClientError, TimeoutError, ValueError):
        logger.exception("Shahar qidiruvida xatolik.")
        return []

    if not isinstance(payload, dict):
        return []

    results = payload.get("results", [])

    if not isinstance(results, list):
        return []

    cities: list[dict[str, Any]] = []

    for item in results:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        country = item.get("country")
        timezone_name = item.get("timezone")

        latitude = item.get("latitude")
        longitude = item.get("longitude")

        if not all(
            isinstance(value, str) and value.strip()
            for value in (name, country, timezone_name)
        ):
            continue

        if not _valid_timezone(timezone_name):
            continue

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            continue

        if not _valid_coordinates(latitude, longitude):
            continue

        cities.append({
            "name": name.strip(),
            "country": country.strip(),
            "timezone": timezone_name.strip(),
            "latitude": latitude,
            "longitude": longitude,
        })

    return cities


def city_results_keyboard(
    cities: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    buttons = []

    for index, city in enumerate(cities):
        buttons.append([
            InlineKeyboardButton(
                text=(
                    f"📍 {city['name']} — {city['country']}"
                ),
                callback_data=f"city:select:{index}",
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons,
    )


async def get_timezone_by_coordinates(
    session: aiohttp.ClientSession,
    latitude: float,
    longitude: float,
) -> str | None:
    if not _valid_coordinates(latitude, longitude):
        return None

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
        "timezone": "auto",
    }

    try:
        async with session.get(
            TIMEZONE_URL,
            params=params,
            timeout=_timeout(),
        ) as response:
            if response.status != 200:
                logger.warning(
                    "Timezone API HTTP status: %s",
                    response.status,
                )
                return None

            payload = await response.json()

        if not isinstance(payload, dict):
            return None

        timezone_name = payload.get("timezone")

        if _valid_timezone(timezone_name):
            return timezone_name.strip()

    except (aiohttp.ClientError, TimeoutError, ValueError):
        logger.exception(
            "Vaqt zonasini aniqlashda xatolik."
        )

    return None


async def reverse_geocode(
    session: aiohttp.ClientSession,
    latitude: float,
    longitude: float,
) -> dict[str, str] | None:
    if not _valid_coordinates(latitude, longitude):
        return None

    params = {
        "format": "jsonv2",
        "lat": latitude,
        "lon": longitude,
        "zoom": 10,
        "addressdetails": 1,
    }

    headers = {
        "User-Agent": "TAQVO-PRO-MAX/1.0",
    }

    try:
        async with session.get(
            REVERSE_URL,
            params=params,
            headers=headers,
            timeout=_timeout(),
        ) as response:
            if response.status != 200:
                logger.warning(
                    "Reverse geocoding HTTP status: %s",
                    response.status,
                )
                return None

            payload = await response.json()

    except (aiohttp.ClientError, TimeoutError, ValueError):
        logger.exception(
            "GPS manzilini aniqlashda xatolik."
        )
        return None

    if not isinstance(payload, dict):
        return None

    address = payload.get("address", {})

    if not isinstance(address, dict):
        return None

    city_name = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or address.get("county")
        or address.get("suburb")
    )

    country = address.get("country")

    if not isinstance(city_name, str) or not city_name.strip():
        return None

    if not isinstance(country, str) or not country.strip():
        return None

    timezone_name = await get_timezone_by_coordinates(
        session,
        latitude,
        longitude,
    )

    if not timezone_name:
        return None

    return {
        "name": city_name.strip(),
        "country": country.strip(),
        "timezone": timezone_name,
    }


async def send_mini_app_button(
    message: Message,
) -> None:
    if not settings.mini_app_url:
        return

    await message.answer(
        "📱 <b>TAQVO PRO MAX</b>\n\n"
        "Mini ilovani ochish uchun quyidagi tugmani bosing:",
        reply_markup=mini_app_keyboard(
            settings.mini_app_url,
        ),
    )


async def save_city(
    message: Message,
    user_id: int,
    city: dict[str, Any],
) -> None:
    name = city.get("name")
    country = city.get("country")
    timezone_name = city.get("timezone")

    if not all(
        isinstance(value, str) and value.strip()
        for value in (name, country, timezone_name)
    ):
        raise ValueError("Shahar ma'lumotlari noto'g'ri.")

    if not _valid_timezone(timezone_name):
        raise ValueError("Vaqt zonasi noto'g'ri.")

    set_location(
        user_id=user_id,
        city=name.strip(),
        country=country.strip(),
        timezone_name=timezone_name.strip(),
    )

    await message.answer(
        "✅ <b>Joylashuvingiz saqlandi!</b>\n\n"
        f"📍 Shahar: <b>{escape(name.strip())}</b>\n"
        f"🌍 Davlat: <b>{escape(country.strip())}</b>\n"
        f"🕒 Vaqt zonasi: "
        f"<code>{escape(timezone_name.strip())}</code>\n\n"
        "Endi namoz vaqtlaringiz shu joylashuv bo‘yicha hisoblanadi.",
        reply_markup=main_keyboard(),
    )

    await send_mini_app_button(message)


@router.message(F.location)
async def gps_location_handler(
    message: Message,
    http_session: aiohttp.ClientSession,
) -> None:
    user = message.from_user
    location = message.location

    if user is None or location is None:
        return

    await message.answer(
        "📍 Joylashuvingiz aniqlanmoqda..."
    )

    city = await reverse_geocode(
        http_session,
        location.latitude,
        location.longitude,
    )

    if not city:
        await message.answer(
            "GPS orqali shaharni aniqlab bo‘lmadi.\n\n"
            "Iltimos, shahar nomini yozib yuboring."
        )
        return

    try:
        await save_city(
            message,
            user.id,
            city,
        )

    except Exception:
        logger.exception(
            "GPS joylashuvini saqlashda xatolik."
        )

        await message.answer(
            "Joylashuvni saqlashda xatolik yuz berdi. "
            "Qayta urinib ko‘ring."
        )


@router.message(Command("city"))
async def city_command_handler(
    message: Message,
) -> None:
    await message.answer(
        "🌍 <b>Shaharni qidirish</b>\n\n"
        "Shahar nomini yuboring.\n\n"
        "Masalan: Karaganda, Tashkent, London, "
        "Istanbul, Makkah."
    )


@router.message(
    F.text
    & ~F.text.startswith("/")
    & ~F.text.in_(RESERVED_TEXTS)
)
async def city_search_handler(
    message: Message,
    http_session: aiohttp.ClientSession,
) -> None:
    user = message.from_user
    query = (message.text or "").strip()

    if user is None or not query:
        return

    if len(query) < 2:
        return

    if len(query) > 100:
        await message.answer(
            "Shahar nomi juda uzun."
        )
        return

    await message.answer(
        "🔎 Dunyo bo‘yicha shahar qidirilmoqda..."
    )

    cities = await search_cities(
        http_session,
        query,
    )

    if not cities:
        await message.answer(
            "❌ Shahar topilmadi.\n"
            "Nomini boshqacha yozib ko‘ring."
        )
        return

    CITY_RESULTS[user.id] = cities

    await message.answer(
        "🌍 <b>Topilgan shaharlar:</b>\n\n"
        "O‘zingizga kerakli shaharni tanlang:",
        reply_markup=city_results_keyboard(cities),
    )


@router.callback_query(
    F.data.startswith("city:select:")
)
async def city_select_handler(
    callback: CallbackQuery,
) -> None:
    user_id = callback.from_user.id
    cities = CITY_RESULTS.get(user_id, [])

    try:
        index = int(
            (callback.data or "").split(":")[-1]
        )

        if not 0 <= index < len(cities):
            raise IndexError

        city = cities[index]

    except (ValueError, IndexError):
        await callback.answer(
            "Qidiruv natijasi eskirgan. "
            "Shaharni qayta qidiring.",
            show_alert=True,
        )
        return

    if not isinstance(callback.message, Message):
        await callback.answer(
            "Xabarni qayta yuboring.",
            show_alert=True,
        )
        return

    try:
        await save_city(
            callback.message,
            user_id,
            city,
        )

        CITY_RESULTS.pop(user_id, None)

        await callback.answer(
            "Joylashuv saqlandi!"
        )

    except Exception:
        logger.exception(
            "Shaharni saqlashda xatolik."
        )

        await callback.answer(
            "Joylashuvni saqlab bo‘lmadi.",
            show_alert=True,
        )
