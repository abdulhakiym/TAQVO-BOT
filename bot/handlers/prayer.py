
from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.types import Message
import aiohttp

from database import get_user
from keyboards import location_keyboard, main_keyboard
from services.prayer_service import (
    PrayerServiceError,
    fetch_prayer_times,
    format_prayer_message,
)


logger = logging.getLogger(__name__)

router = Router(name="prayer")


@router.message(F.text == "🕌 Namoz vaqtlarim")
async def prayer_times_handler(
    message: Message,
    http_session: aiohttp.ClientSession,
) -> None:
    """Foydalanuvchining shahriga mos namoz vaqtlarini chiqaradi."""

    user = message.from_user

    if user is None:
        return

    try:
        profile = get_user(user.id)

        if not profile:
            await message.answer(
                "Avval botni ishga tushiring: /start"
            )
            return

        city = profile.get("city")
        country = profile.get("country")
        timezone_name = profile.get("timezone")
        method = profile.get("prayer_method")

        if not city or not country:
            await message.answer(
                "📍 Namoz vaqtlarini ko‘rsatish uchun "
                "avval shahringizni tanlang.",
                reply_markup=location_keyboard(),
            )
            return

        await message.answer("🕌 Namoz vaqtlari yuklanmoqda...")

        prayer = await fetch_prayer_times(
            session=http_session,
            city=city,
            country=country,
            method=method,
            timezone_name=timezone_name,
        )

        await message.answer(
            format_prayer_message(prayer),
            reply_markup=main_keyboard(),
        )

    except PrayerServiceError as error:
        logger.warning(
            "Namoz vaqti xizmati xatoligi: %s",
            error,
        )
        await message.answer(
            "Namoz vaqtlarini hozircha olib bo‘lmadi.\n"
            "Iltimos, birozdan keyin qayta urinib ko‘ring.",
            reply_markup=main_keyboard(),
        )

    except Exception:
        logger.exception(
            "Namoz vaqtlarini chiqarishda xatolik. User ID: %s",
            user.id,
        )
        await message.answer(
            "Texnik xatolik yuz berdi. "
            "Iltimos, keyinroq qayta urinib ko‘ring.",
            reply_markup=main_keyboard(),
        )
