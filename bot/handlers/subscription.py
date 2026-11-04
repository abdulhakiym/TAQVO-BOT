
from __future__ import annotations

import logging

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from database import set_subscription
from keyboards import location_keyboard
from services.subscription_service import check_subscription


logger = logging.getLogger(__name__)

router = Router(name="subscription")


@router.callback_query(F.data == "subscription:check")
async def subscription_check_handler(
    callback: CallbackQuery,
    bot: Bot,
) -> None:
    """Kanal obunasini qayta tekshiradi."""

    user = callback.from_user

    try:
        is_subscribed = await check_subscription(
            bot=bot,
            user_id=user.id,
        )

        if not is_subscribed:
            await callback.answer(
                "❌ Siz hali kanalga obuna bo‘lmagansiz. "
                "Avval kanalga obuna bo‘ling.",
                show_alert=True,
            )
            return

        set_subscription(user.id, True)

        await callback.answer(
            "✅ Obuna tasdiqlandi!"
        )

        if isinstance(callback.message, Message):
            await callback.message.answer(
                "Assalomu alaykum va rohmatullohi va barokatuh!\n\n"
                "🕌 <b>TAQVO PRO MAX</b> xizmatiga xush kelibsiz.\n\n"
                "Endi namoz vaqtlarini hisoblash uchun "
                "joylashuvingizni tanlang.\n\n"
                "📍 Joylashuvingizni yuboring yoki "
                "shaharni qo‘lda kiriting.",
                reply_markup=location_keyboard(),
            )

    except Exception:
        logger.exception(
            "Obuna callback xatoligi. User ID: %s",
            user.id,
        )

        await callback.answer(
            "Texnik xatolik yuz berdi. Qayta urinib ko‘ring.",
            show_alert=True,
        )
