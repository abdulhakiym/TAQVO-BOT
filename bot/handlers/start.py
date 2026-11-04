from __future__ import annotations

import logging
from html import escape

from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import settings
from database import create_user, set_subscription
from keyboards import location_keyboard, subscription_keyboard
from services.subscription_service import check_subscription


logger = logging.getLogger(__name__)

router = Router(name="start")


WELCOME_TEXT = (
    "Assalomu alaykum va rohmatullohi va barokatuh!\n\n"
    "🕌 <b>TAQVO PRO MAX</b> xizmatiga xush kelibsiz.\n\n"
)


async def show_start_screen(
    message: Message,
    bot: Bot,
    user_id: int,
) -> None:
    """Obunani tekshiradi va foydalanuvchini kerakli bosqichga olib boradi."""

    is_subscribed = await check_subscription(bot, user_id)

    if not is_subscribed:
        set_subscription(user_id, False)

        await message.answer(
            WELCOME_TEXT
            + "Botning barcha imkoniyatlaridan foydalanish uchun "
            "rasmiy Telegram kanalimizga obuna bo‘ling:\n\n"
            f"📢 <b>{escape(settings.channel_username)}</b>\n\n"
            "Obuna bo‘lganingizdan keyin "
            "«Obunani tekshirish» tugmasini bosing.",
            reply_markup=subscription_keyboard(settings.channel_url),
        )
        return

    set_subscription(user_id, True)

    await message.answer(
        WELCOME_TEXT
        + "Namoz vaqtlarini to‘g‘ri hisoblash uchun "
        "avval joylashuvingizni tanlang.\n\n"
        "📍 GPS orqali joylashuvingizni yuboring "
        "yoki shahar nomini yozing.",
        reply_markup=location_keyboard(),
    )


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
) -> None:
    user = message.from_user

    if user is None:
        return

    try:
        create_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )

        await show_start_screen(
            message=message,
            bot=bot,
            user_id=user.id,
        )

    except Exception:
        logger.exception(
            "Start buyrug‘ida xatolik. User ID: %s",
            user.id,
        )

        await message.answer(
            "⚠️ Hozircha xizmatda texnik xatolik yuz berdi.\n\n"
            "Iltimos, birozdan keyin /start buyrug‘ini qayta yuboring."
        )
