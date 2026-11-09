"""TAQVO BOT start and subscription handlers."""

import logging

from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    User as TelegramUser,
    WebAppInfo,
)
from sqlalchemy.exc import SQLAlchemyError

from bot.config import get_settings
from bot.services.user_service import register_or_update_user


logger = logging.getLogger(__name__)

router = Router(name="start")


def subscription_keyboard() -> InlineKeyboardMarkup:
    """Create the mandatory channel subscription keyboard."""

    settings = get_settings()
    channel = settings.channel_username.lstrip("@")

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo'lish",
                    url=f"https://t.me/{channel}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="check_subscription",
                )
            ],
        ]
    )


def mini_app_keyboard() -> InlineKeyboardMarkup | None:
    """Create the Mini App launch keyboard."""

    settings = get_settings()
    webapp_url = settings.webapp_url.strip()

    if not webapp_url:
        logger.warning("WEBAPP_URL sozlanmagan.")
        return None

    if not webapp_url.startswith("https://"):
        logger.error("WEBAPP_URL HTTPS manzil bo'lishi kerak.")
        return None

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 TAQVO PRO MAX'ni ochish",
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ]
    )


async def check_user_subscription(
    bot: Bot,
    user_id: int,
) -> bool | None:
    """
    True: subscribed.
    False: not subscribed.
    None: Telegram API verification failed.
    """

    settings = get_settings()

    try:
        member = await bot.get_chat_member(
            chat_id=settings.channel_username,
            user_id=user_id,
        )

        if member.status in {
            "creator",
            "administrator",
            "member",
        }:
            return True

        if member.status == "restricted":
            return bool(
                getattr(member, "is_member", False)
            )

        return False

    except TelegramAPIError:
        logger.exception(
            "Subscription check failed for user %s",
            user_id,
        )
        return None


async def save_telegram_user(
    telegram_user: TelegramUser,
) -> bool:
    """Save the actual Telegram user in PostgreSQL."""

    language = telegram_user.language_code

    if language not in {"uz", "uz-Cyrl", "ru"}:
        language = None

    try:
        await register_or_update_user(
            telegram_id=telegram_user.id,
            first_name=telegram_user.first_name,
            username=telegram_user.username,
            language=language,
        )

        logger.info(
            "User %s saved successfully.",
            telegram_user.id,
        )
        return True

    except (SQLAlchemyError, ValueError):
        logger.exception(
            "Could not save Telegram user %s",
            telegram_user.id,
        )
        return False


async def send_access_message(
    message: Message,
    bot: Bot,
) -> None:
    """Check subscription, save the user and show Mini App access."""

    telegram_user = message.from_user

    if telegram_user is None:
        return

    is_subscribed = await check_user_subscription(
        bot=bot,
        user_id=telegram_user.id,
    )

    if is_subscribed is None:
        await message.answer(
            "⚠️ Obunani tekshirishda xatolik yuz berdi.\n"
            "Iltimos, birozdan keyin qayta urinib ko'ring."
        )
        return

    if not is_subscribed:
        await message.answer(
            "Assalomu alaykum!\n\n"
            "TAQVO BOT xizmatlaridan foydalanish uchun "
            "@hakiymqalb kanaliga obuna bo'ling.\n\n"
            "Obuna bo'lgach, tekshirish tugmasini bosing.",
            reply_markup=subscription_keyboard(),
        )
        return

    saved = await save_telegram_user(telegram_user)

    if not saved:
        await message.answer(
            "⚠️ Obunangiz tasdiqlandi, lekin ma'lumotlaringizni "
            "saqlashda vaqtinchalik xatolik yuz berdi.\n\n"
            "Iltimos, birozdan keyin /start buyrug'ini qayta yuboring."
        )
        return

    keyboard = mini_app_keyboard()

    if keyboard is None:
        await message.answer(
            "Alhamdulillah! Obunangiz tasdiqlandi.\n\n"
            "Foydalanuvchi ma'lumotlaringiz saqlandi.\n"
            "TAQVO PRO MAX Mini App manzili hali sozlanmagan "
            "yoki noto'g'ri sozlangan."
        )
        return

    await message.answer(
        "Assalomu alaykum!\n\n"
        "TAQVO BOT'ga xush kelibsiz!\n"
        "✅ Obunangiz tasdiqlandi.\n"
        "✅ Ma'lumotlaringiz saqlandi.\n\n"
        "TAQVO PRO MAX xizmatlaridan foydalanishingiz mumkin.",
        reply_markup=keyboard,
    )


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
) -> None:
    """Handle the /start command."""

    await send_access_message(message, bot)


@router.callback_query(
    lambda query: query.data == "check_subscription"
)
async def subscription_callback(
    callback: CallbackQuery,
    bot: Bot,
) -> None:
    """Handle the subscription verification button."""

    telegram_user = callback.from_user

    if not isinstance(callback.message, Message):
        await callback.answer(
            "Xabarni qayta ochib urinib ko'ring.",
            show_alert=True,
        )
        return

    is_subscribed = await check_user_subscription(
        bot=bot,
        user_id=telegram_user.id,
    )

    if is_subscribed is None:
        await callback.answer(
            "Tekshirish vaqtida xatolik yuz berdi.",
            show_alert=True,
        )
        return

    if not is_subscribed:
        await callback.answer(
            "Siz hali kanalga obuna bo'lmagansiz!",
            show_alert=True,
        )
        return

    saved = await save_telegram_user(telegram_user)

    if not saved:
        await callback.answer(
            "Ma'lumotlarni saqlashda xatolik yuz berdi.",
            show_alert=True,
        )
        return

    await callback.answer("Obuna tasdiqlandi!")

    keyboard = mini_app_keyboard()

    if keyboard is None:
        await callback.message.answer(
            "Alhamdulillah! Obunangiz tasdiqlandi "
            "va ma'lumotlaringiz saqlandi.\n\n"
            "Mini App manzili hali sozlanmagan."
        )
        return

    await callback.message.answer(
        "Alhamdulillah! Obunangiz tasdiqlandi.\n"
        "Ma'lumotlaringiz bazaga saqlandi.",
        reply_markup=keyboard,
    )
