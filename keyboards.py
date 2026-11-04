from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import settings


def subscription_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="📢 Kanalga obuna bo‘lish",
            url=f"https://t.me/{settings.CHANNEL_USERNAME.lstrip('@')}",
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="✅ Obunani tasdiqlash",
            callback_data="subscription:check",
        )
    )

    return builder.as_markup()


def country_keyboard() -> InlineKeyboardMarkup:
    countries = [
        ("🇺🇿 O‘zbekiston", "UZ"),
        ("🇰🇿 Qozog‘iston", "KZ"),
        ("🇰🇬 Qirg‘iziston", "KG"),
        ("🇹🇯 Tojikiston", "TJ"),
        ("🇹🇷 Turkiya", "TR"),
        ("🇸🇦 Saudiya Arabistoni", "SA"),
        ("🇷🇺 Rossiya", "RU"),
        ("🇦🇪 BAA", "AE"),
    ]

    builder = InlineKeyboardBuilder()

    for title, code in countries:
        builder.button(
            text=title,
            callback_data=f"country:{code}",
        )

    builder.adjust(2)

    builder.row(
        InlineKeyboardButton(
            text="🌍 Boshqa davlat",
            callback_data="country:other",
        )
    )

    return builder.as_markup()


def city_search_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🔎 Shaharni qidirish",
            callback_data="city:search",
        )
    )

    builder.row(
        InlineKeyboardButton(
            text="📍 Joylashuvimni yuborish",
            callback_data="city:location",
        )
    )

    return builder.as_markup()


def city_results_keyboard(
    cities: list[dict],
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for city in cities:
        builder.button(
            text=f"📍 {city['name']}, {city['country']}",
            callback_data=f"city:select:{city['id']}",
        )

    builder.adjust(1)

    return builder.as_markup()


def mini_app_keyboard() -> InlineKeyboardMarkup:
    if not settings.MINI_APP_URL:
        raise RuntimeError(
            "MINI_APP_URL sozlanmagan"
        )

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="🚀 TAQVO PRO MAX ilovasini ochish",
            web_app=WebAppInfo(
                url=settings.MINI_APP_URL
            ),
        )
    )

    return builder.as_markup()


def location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📍 Joylashuvimni yuborish",
                    request_location=True,
                )
            ],
            [
                KeyboardButton(
                    text="Shaharni qo‘lda tanlash"
                )
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
