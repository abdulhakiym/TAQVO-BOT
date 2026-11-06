
from aiogram import Bot, Router
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from bot.config import get_settings


router = Router(name="start")


def subscription_keyboard() -> InlineKeyboardMarkup:
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
    settings = get_settings()

    if not settings.mini_app_url:
        return None

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 TAQVO PRO MAX'ni ochish",
                    web_app=WebAppInfo(url=settings.mini_app_url),
                )
            ]
        ]
    )


async def check_user_subscription(
    bot: Bot,
    user_id: int,
) -> bool | None:
    """Return True/False; None means Telegram API verification failed."""

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
            return bool(getattr(member, "is_member", False))

        return False

    except TelegramAPIError:
        return None


async def send_access_message(
    message: Message,
    bot: Bot,
) -> None:
    if not message.from_user:
        return

    is_subscribed = await check_user_subscription(
        bot=bot,
        user_id=message.from_user.id,
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

    keyboard = mini_app_keyboard()

    if keyboard is None:
        await message.answer(
            "Alhamdulillah! Obunangiz tasdiqlandi.\n\n"
            "TAQVO PRO MAX Mini App manzili hali sozlanmagan. "
            "Iltimos, administrator bilan bog'laning."
        )
        return

    await message.answer(
        "Assalomu alaykum!\n\n"
        "TAQVO BOT'ga xush kelibsiz!\n"
        "Obunangiz tasdiqlandi.\n\n"
        "TAQVO PRO MAX xizmatlaridan foydalanishingiz mumkin.",
        reply_markup=keyboard,
    )


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot: Bot,
) -> None:
    await send_access_message(message, bot)


@router.callback_query(
    lambda query: query.data == "check_subscription"
)
async def subscription_callback(
    callback: CallbackQuery,
    bot: Bot,
) -> None:
    if not callback.from_user or not callback.message:
        await callback.answer()
        return

    is_subscribed = await check_user_subscription(
        bot=bot,
        user_id=callback.from_user.id,
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

    await callback.answer("Obuna tasdiqlandi!")

    await callback.message.answer(
        "Alhamdulillah! Obunangiz tasdiqlandi.",
        reply_markup=mini_app_keyboard(),
    )
