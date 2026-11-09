
"""TAQVO BOT start and subscription keyboards."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)

from bot.config import get_settings


def subscription_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for channel subscription verification."""

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
    """Keyboard for opening TAQVO PRO MAX Mini App."""

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
