
from __future__ import annotations

import logging
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
from keyboards import main_keyboard


logger = logging.getLogger(__name__)

router = Router(name="location")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Qidiruv natijalarini foydalanuvchi bo‘yicha vaqtincha saqlash.
CITY_RESULTS: dict[int, list[dict[str, Any]]] = {}


async def search_cities(
    session: aiohttp.ClientSession,
    query: str,
) -> list[dict[str, Any]]:
    """Open-Meteo orqali dunyo shaharlarini qidiradi."""

    params = {
        "name": query,
        "count": 8,
        "language": "en",
        "format": "json",
    }

    timeout = aiohttp.ClientTimeout(
        total=settings.http_timeout_seconds
    )

    try:
        async with session.get(
            GEOCODING_URL,
            params=params,
            timeout=timeout,
        ) as response:
            if response.status != 200:
                return []

            payload = await response.json()

    except (aiohttp.ClientError, TimeoutError, ValueError):
        logger.exception("Shahar qidiruvida xatolik.")
        return []

    results = payload.get("results", [])

    if not isinstance(results, list):
        return []

    cities = []

    for item in results:
        if not isinstance(item, dict):
            continue

        name = item.get("name")
        country = item.get("country")
        timezone_name = item.get("timezone")

        if not all(
            isinstance(value, str) and value.strip()
            for value in (name, country, timezone_name)
        ):
            continue

        cities.append({
            "name": name,
            "country": country,
            "timezone": timezone_name,
        })

    return cities


def city_results_keyboard(
    cities: list[dict[str, Any]],
) -> InlineKeyboardMarkup:
    buttons = []

    for index, city in enumerate(cities):
        buttons.append([
            InlineKeyboardButton(
                text=f"📍 {city['name']} — {city['country']}",
                callback_data=f"city:select:{index}",
            )
        ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


async def save_city(
    message: Message,
    user_id: int,
    city: dict[str, Any],
) -> None:
    """Tanlangan shaharni foydalanuvchi bazasiga saqlaydi."""

    set_location(
        user_id=user_id,
        city=city["name"],
        country=city["country"],
        timezone_name=city["timezone"],
    )

    await message.answer(
        "✅ <b>Joylashuvingiz saqlandi!</b>\n\n"
        f"📍 Shahar: <b>{city['name']}</b>\n"
        f"🌍 Davlat: <b>{city['country']}</b>\n"
        f"🕒 Vaqt zonasi: <code>{city['timezone']}</code>\n\n"
        "Endi namoz vaqtlaringiz shu joylashuv bo‘yicha hisoblanadi.",
        reply_markup=main_keyboard(),
    )


@router.message(F.location)
async def gps_location_handler(
    message: Message,
    http_session: aiohttp.ClientSession,
) -> None:
    """GPS koordinatalarini qabul qiladi va yaqin shaharni topadi."""

    user = message.from_user
    location = message.location

    if user is None or location is None:
        return

    await message.answer("📍 Joylashuvingiz aniqlanmoqda...")

    # Open-Meteo reverse geocoding.
    url = "https://geocoding-api.open-meteo.com/v1/reverse"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "language": "en",
        "format": "json",
    }

    try:
        timeout = aiohttp.ClientTimeout(
            total=settings.http_timeout_seconds
        )

        async with http_session.get(
            url,
            params=params,
            timeout=timeout,
        ) as response:
            if response.status != 200:
                raise ValueError("GPS geocoding xatoligi")

            payload = await response.json()

        results = payload.get("results", [])

        if not results:
            await message.answer(
                "Shahringiz aniqlanmadi. "
                "Iltimos, shahar nomini qo‘lda yuboring."
            )
            return

        result = results[0]

        city_name = (
            result.get("name")
            or result.get("city")
            or result.get("town")
            or result.get("village")
        )
        country = result.get("country")
        timezone_name = result.get("timezone")

        if not city_name or not country or not timezone_name:
            await message.answer(
                "Joylashuv ma’lumotlari to‘liq aniqlanmadi. "
                "Shahar nomini qo‘lda yuboring."
            )
            return

        await save_city(
            message,
            user.id,
            {
                "name": city_name,
                "country": country,
                "timezone": timezone_name,
            },
        )

    except Exception:
        logger.exception("GPS joylashuvini aniqlashda xatolik.")
        await message.answer(
            "GPS orqali joylashuv aniqlanmadi. "
            "Shahar nomini qo‘lda yuboring."
        )


@router.message(Command("city"))
async def city_command_handler(message: Message) -> None:
    await message.answer(
        "🌍 <b>Shaharni qidirish</b>\n\n"
        "Shahar nomini yuboring.\n"
        "Masalan: Karaganda, London, Istanbul, Makkah."
    )


@router.message(F.text)
async def city_search_handler(
    message: Message,
    http_session: aiohttp.ClientSession,
) -> None:
    """Foydalanuvchi yozgan shaharni dunyo bo‘yicha qidiradi."""

    user = message.from_user
    query = (message.text or "").strip()

    if user is None or not query:
        return

    if query.startswith("/"):
        return

    if len(query) < 2:
        await message.answer("Shahar nomini to‘liqroq yozing.")
        return

    if len(query) > 100:
        await message.answer("Shahar nomi juda uzun.")
        return

    await message.answer("🔎 Dunyo bo‘yicha shahar qidirilmoqda...")

    cities = await search_cities(http_session, query)

    if not cities:
        await message.answer(
            "❌ Shahar topilmadi. Nomini boshqacha yozib ko‘ring."
        )
        return

    CITY_RESULTS[user.id] = cities

    await message.answer(
        "🌍 <b>Topilgan shaharlar:</b>\n\n"
        "O‘zingizga kerakli shaharni tanlang:",
        reply_markup=city_results_keyboard(cities),
    )


@router.callback_query(F.data.startswith("city:select:"))
async def city_select_handler(
    callback: CallbackQuery,
) -> None:
    """Qidiruv natijasidan tanlangan shaharni saqlaydi."""

    user_id = callback.from_user.id
    cities = CITY_RESULTS.get(user_id, [])

    try:
        index = int(callback.data.split(":")[-1])
        city = cities[index]
    except (ValueError, IndexError, AttributeError):
        await callback.answer(
            "Qidiruv natijasi eskirgan. Shaharni qayta qidiring.",
            show_alert=True,
        )
        return

    if not isinstance(callback.message, Message):
        await callback.answer("Xabarni qayta yuboring.")
        return

    try:
        set_location(
            user_id=user_id,
            city=city["name"],
            country=city["country"],
            timezone_name=city["timezone"],
        )

        CITY_RESULTS.pop(user_id, None)

        await callback.answer("Joylashuv saqlandi!")

        await callback.message.answer(
            "✅ <b>Joylashuvingiz saqlandi!</b>\n\n"
            f"📍 Shahar: <b>{city['name']}</b>\n"
            f"🌍 Davlat: <b>{city['country']}</b>\n"
            f"🕒 Vaqt zonasi: <code>{city['timezone']}</code>\n\n"
            "Namoz vaqtlari shu joylashuv bo‘yicha hisoblanadi.",
            reply_markup=main_keyboard(),
        )

    except Exception:
        logger.exception("Shaharni saqlashda xatolik.")
        await callback.answer(
            "Joylashuvni saqlab bo‘lmadi.",
            show_alert=True,
        )
