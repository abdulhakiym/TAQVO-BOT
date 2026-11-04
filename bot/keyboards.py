
"""TAQVO PRO MAX — Telegram bot klaviaturalari."""
from __future__ import annotations

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)


def subscription_keyboard(
    channel_url: str,
) -> InlineKeyboardMarkup:
    """Majburiy kanal obunasi tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url=channel_url,
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="subscription:check",
                )
            ],
        ]
    )


def main_keyboard() -> ReplyKeyboardMarkup:
    """Botdagi doimiy pastki menyu."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🕌 Namoz vaqtlarim",
                )
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Namoz vaqtlarini ko‘rish",
    )


def mini_app_keyboard(
    mini_app_url: str,
) -> InlineKeyboardMarkup:
    """TAQVO PRO MAX Mini App ochish tugmasi."""
    if not mini_app_url.startswith("https://"):
        raise ValueError(
            "Mini App manzili HTTPS bilan boshlanishi kerak."
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌿 TAQVO PRO MAX — ochish",
                    web_app=WebAppInfo(url=mini_app_url),
                )
            ]
        ]
    )


def location_keyboard() -> ReplyKeyboardMarkup:
    """GPS orqali joylashuv yuborish."""
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
                    text="✍️ Shaharni qo‘lda kiritish",
                )
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Joylashuvingizni tanlang",
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """Kiritish jarayonini bekor qilish."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="❌ Bekor qilish"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def settings_keyboard() -> InlineKeyboardMarkup:
    """Foydalanuvchi sozlamalari menyusi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📍 Shaharni o‘zgartirish",
                    callback_data="settings:location",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🕰 Hisoblash usuli",
                    callback_data="settings:prayer_method",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔔 Eslatmalar",
                    callback_data="settings:reminders",
                )
            ],
        ]
    )


def prayer_method_keyboard() -> InlineKeyboardMarkup:
    """Namoz vaqtlarini hisoblash usullari."""
    methods = [
        (0, "Shia Ithna-Ashari"),
        (1, "University of Islamic Sciences, Karachi"),
        (2, "Islamic Society of North America"),
        (3, "Muslim World League"),
        (4, "Umm Al-Qura University, Makkah"),
        (5, "Egyptian General Authority"),
        (7, "Institute of Geophysics, Tehran"),
        (8, "Gulf Region"),
        (9, "Kuwait"),
        (10, "Qatar"),
        (11, "Singapore"),
        (12, "France"),
        (13, "Turkey"),
        (14, "Russia"),
        (15, "Moonsighting Committee"),
        (16, "Dubai"),
        (17, "JAKIM Malaysia"),
        (18, "Tunisia"),
        (19, "Algeria"),
        (20, "Indonesia"),
        (21, "Morocco"),
        (22, "Portugal"),
        (23, "Jordan"),
    ]

    rows = [
        [
            InlineKeyboardButton(
                text=name,
                callback_data=f"prayer_method:{method_id}",
            )
        ]
        for method_id, name in methods
    ]

    return InlineKeyboardMarkup(inline_keyboard=rows)


def reminder_keyboard(enabled: bool) -> InlineKeyboardMarkup:
    """Eslatmalarni yoqish yoki o‘chirish."""
    action = "reminders:disable" if enabled else "reminders:enable"
    label = (
        "🔕 Eslatmalarni o‘chirish"
        if enabled
        else "🔔 Eslatmalarni yoqish"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=label,
                    callback_data=action,
                )
            ]
        ]
    )


def tasbeh_keyboard() -> InlineKeyboardMarkup:
    """Tasbeh hisoblagichi tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📿 +1",
                    callback_data="tasbeh:add",
                ),
                InlineKeyboardButton(
                    text="🔄 Nolga tushirish",
                    callback_data="tasbeh:reset",
                ),
            ]
        ]
    )


def quiz_answer_keyboard(
    question_id: str,
    answers: list[str],
) -> InlineKeyboardMarkup:
    """Siyrat viktorinasi javoblari."""
    if not question_id or len(question_id) > 64:
        raise ValueError("Savol ID noto‘g‘ri.")

    if not 2 <= len(answers) <= 6:
        raise ValueError("Javoblar soni 2 dan 6 gacha bo‘lishi kerak.")

    rows = []

    for index, answer in enumerate(answers):
        if not answer.strip():
            raise ValueError("Javob bo‘sh bo‘lmasligi kerak.")

        rows.append(
            [
                InlineKeyboardButton(
                    text=answer[:64],
                    callback_data=f"quiz:{question_id}:{index}",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)
