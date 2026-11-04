from __future__ import annotations

import logging

import aiohttp
from aiogram import Bot, F, Router
from aiogram.types import Message

from config import settings
from database import get_user, set_subscription
from keyboards import (
    location_keyboard,
    main_keyboard,
    subscription_keyboard,
)
from services.prayer_service import (
    PrayerServiceError,
    fetch_prayer_times,
    format_prayer_message,
)
from services.subscription_service import check_subscription


logger = logging.getLogger(__name__)

router = Router(name="prayer")


@router.message(F.text == "🕌 Namoz vaqtlarim")
async def prayer_times_handler(
    message: Message,
    bot: Bot,
    http_session: aiohttp.ClientSession,
) -> None:
    """Obunani tekshiradi va namoz vaqtlarini ko‘rsatadi."""

    user = message.from_user

    if user is None:
        return

    try:
        profile = get_user(user.id)

        if not profile:
            await message.answer(
                "Avval /start buyrug‘i orqali botni ishga tushiring."
            )
            return

        # Kanal obunasini qayta tekshirish.
        is_subscribed = await check_subscription(
            bot=bot,
            user_id=user.id,
        )

        if not is_subscribed:
            set_subscription(user.id, False)

            await message.answer(
                "🔒 <b>Botdan foydalanish uchun kanalga obuna bo‘ling.</b>\n\n"
                f"📢 {settings.channel_username}\n\n"
                "Obuna bo‘lgach, «Obunani tekshirish» tugmasini bosing.",
                reply_markup=subscription_keyboard(settings.channel_url),
            )
            return

        set_subscription(user.id, True)

        city = profile.get("city")
        country = profile.get("country")
        timezone_name = profile.get("timezone")
        prayer_method = profile.get("prayer_method")

        if not city or not country:
            await message.answer(
                "📍 <b>Joylashuvingiz hali saqlanmagan.</b>\n\n"
                "Namoz vaqtlarini hisoblash uchun shahringizni "
                "tanlang yoki GPS joylashuvingizni yuboring.",
                reply_markup=location_keyboard(),
            )
            return

        await message.answer("🕌 Namoz vaqtlari hisoblanmoqda...")

        prayer_times = await fetch_prayer_times(
            session=http_session,
            city=city,
            country=country,
            method=prayer_method,
            timezone_name=timezone_name,
        )

        await message.answer(
            format_prayer_message(prayer_times),
            reply_markup=main_keyboard(),
        )

    except PrayerServiceError as error:
        logger.warning(
            "Namoz vaqtlarini olishda xatolik: %s",
            error,
        )

        await message.answer(
            "⚠️ Namoz vaqtlarini hozircha olish imkoni bo‘lmadi.\n\n"
            "Iltimos, birozdan keyin qayta urinib ko‘ring.",
            reply_markup=main_keyboard(),
        )

    except (aiohttp.ClientError, TimeoutError):
        logger.exception("Namoz API bilan aloqa xatoligi.")

        await message.answer(
            "🌐 Internet yoki server bilan aloqa uzildi.\n"
            "Iltimos, keyinroq qayta urinib ko‘ring.",
            reply_markup=main_keyboard(),
        )

    except Exception:
        logger.exception(
            "Namoz vaqtlarini ko‘rsatishda kutilmagan xatolik."
        )

        await message.answer(
            "❌ Kutilmagan xatolik yuz berdi.\n"
            "Iltimos, keyinroq qayta urinib ko‘ring.",
            reply_markup=main_keyboard(),
        )
