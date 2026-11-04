from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from database import get_user, set_subscription
from keyboards import location_keyboard
from services.subscription_service import check_subscription


logger = logging.getLogger(__name__)

router = Router(name="subscription")


@router.callback_query(F.data == "subscription:check")
async def subscription_check_handler(
    callback: CallbackQuery,
    bot: Bot,
) -> None:
    """Telegram kanaliga obunani qayta tekshiradi."""

    user_id = callback.from_user.id
    answered = False

    try:
        profile = get_user(user_id)

        if not profile:
            await callback.answer(
                "Avval /start buyrug‘ini bosing.",
                show_alert=True,
            )
            return

        is_subscribed = await check_subscription(
            bot=bot,
            user_id=user_id,
        )

        if not is_subscribed:
            await callback.answer(
                "❌ Siz hali kanalga obuna bo‘lmagansiz. "
                "Avval kanalga obuna bo‘ling.",
                show_alert=True,
            )
            return

        set_subscription(user_id, True)

        await callback.answer("✅ Obuna tasdiqlandi!")
        answered = True

        if isinstance(callback.message, Message):
            await callback.message.answer(
                "Assalomu alaykum va rohmatullohi va barokatuh!\n\n"
                "🕌 <b>TAQVO PRO MAX</b> xizmatiga xush kelibsiz.\n\n"
                "Endi namoz vaqtlarini hisoblash uchun "
                "joylashuvingizni tanlang.\n\n"
                "📍 GPS orqali joylashuvingizni yuboring "
                "yoki shahar nomini yozing.",
                reply_markup=location_keyboard(),
            )

    except Exception:
        logger.exception(
            "Obuna tekshiruvida xatolik. User ID: %s",
            user_id,
        )

        if not answered:
            await callback.answer(
                "Texnik xatolik yuz berdi. Qayta urinib ko‘ring.",
                show_alert=True,
            )

        elif isinstance(callback.message, Message):
            await callback.message.answer(
                "⚠️ Texnik xatolik yuz berdi. "
                "Iltimos, /start buyrug‘ini qayta yuboring."
            )
