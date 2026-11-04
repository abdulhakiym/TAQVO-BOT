"""
TAQVO PRO MAX — Telegram bot klaviaturalari.
Aiogram 3.x
"""

from __future__ import annotations

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)


PRAYER_METHODS = [
    (0, "Shia Ithna-Ashari"),
    (1, "Karachi"),
    (2, "ISNA"),
    (3, "Muslim World League"),
    (4, "Umm Al-Qura, Makkah"),
    (5, "Egypt"),
    (7, "Tehran"),
    (8, "Gulf Region"),
    (9, "Kuwait"),
    (10, "Qatar"),
    (11, "Singapore"),
    (12, "France"),
    (13, "Turkey"),
    (14, "Russia"),
    (15, "Moonsighting Committee"),
    (16, "Dubai"),
    (17, "Malaysia"),
    (18, "Tunisia"),
    (19, "Algeria"),
    (20, "Indonesia"),
    (21, "Morocco"),
    (22, "Portugal"),
    (23, "Jordan"),
]


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
    """Botning doimiy pastki menyusi."""

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
    """TAQVO PRO MAX Mini App tugmasi."""

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
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="GPS yuboring yoki shahar nomini yozing",
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    """Jarayonni bekor qilish tugmasi."""

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="❌ Bekor qilish",
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def settings_keyboard() -> InlineKeyboardMarkup:
    """Foydalanuvchi sozlamalari."""

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
                    text="🕌 Namoz hisoblash usuli",
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
    """Namoz hisoblash usulini tanlash."""

    rows = []

    for method_id, method_name in PRAYER_METHODS:
        rows.append(
            [
                InlineKeyboardButton(
                    text=method_name,
                    callback_data=f"settings:method:{method_id}",
                )
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data="settings:back",
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )


def reminder_keyboard(
    enabled: bool,
) -> InlineKeyboardMarkup:
    """Eslatmalarni yoqish yoki o‘chirish."""

    if enabled:
        label = "🔕 Eslatmalarni o‘chirish"
        callback = "settings:reminders:off"
    else:
        label = "🔔 Eslatmalarni yoqish"
        callback = "settings:reminders:on"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=label,
                    callback_data=callback,
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Orqaga",
                    callback_data="settings:back",
                )
            ],
        ]
    )


def tasbeh_keyboard() -> InlineKeyboardMarkup:
    """Tasbeh hisoblagichi."""

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

    if not question_id or len(question_id) > 40:
        raise ValueError("Savol ID noto‘g‘ri.")

    if not 2 <= len(answers) <= 6:
        raise ValueError(
            "Javoblar soni 2 dan 6 gacha bo‘lishi kerak."
        )

    rows = []

    for index, answer in enumerate(answers):
        if not answer.strip():
            raise ValueError(
                "Javob bo‘sh bo‘lmasligi kerak."
            )

        rows.append(
            [
                InlineKeyboardButton(
                    text=answer[:64],
                    callback_data=f"quiz:{question_id}:{index}",
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=rows
    )
