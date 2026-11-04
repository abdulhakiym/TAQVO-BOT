
from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from config import settings
from database import (
    get_user,
    set_prayer_method,
    set_reminders,
)
from keyboards import location_keyboard, main_keyboard


logger = logging.getLogger(__name__)

router = Router(name="settings")


PRAYER_METHODS = [
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
    (11, "Majlis Ugama Islam Singapura"),
    (12, "Union Organization Islamic de France"),
    (13, "Diyanet İşleri Başkanlığı, Turkey"),
    (14, "Spiritual Administration of Muslims of Russia"),
    (15, "Moonsighting Committee"),
    (16, "Dubai"),
    (17, "Jabatan Kemajuan Islam Malaysia"),
    (18, "Tunisia"),
    (19, "Algeria"),
    (20, "Kementerian Agama Indonesia"),
    (21, "Morocco"),
    (22, "Comunidade Islamica de Lisboa"),
    (23, "Jordan"),
]


def settings_menu() -> InlineKeyboardMarkup:
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


def prayer_methods_menu() -> InlineKeyboardMarkup:
    buttons = []

    for method_id, method_name in PRAYER_METHODS:
        buttons.append([
            InlineKeyboardButton(
                text=method_name,
                callback_data=f"settings:method:{method_id}",
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="⬅️ Sozlamalarga qaytish",
            callback_data="settings:back",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def reminders_menu(enabled: bool) -> InlineKeyboardMarkup:
    if enabled:
        button_text = "🔕 Eslatmalarni o‘chirish"
        callback_data = "settings:reminders:off"
    else:
        button_text = "🔔 Eslatmalarni yoqish"
        callback_data = "settings:reminders:on"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=callback_data,
                )
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Sozlamalarga qaytish",
                    callback_data="settings:back",
                )
            ],
        ]
    )


@router.message(Command("settings"))
async def settings_command(message: Message) -> None:
    await message.answer(
        "⚙️ <b>TAQVO PRO MAX — SOZLAMALAR</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=settings_menu(),
    )


@router.callback_query(F.data == "settings:back")
async def settings_back(callback: CallbackQuery) -> None:
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "⚙️ <b>Sozlamalar</b>\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=settings_menu(),
        )


@router.callback_query(F.data == "settings:location")
async def change_location(callback: CallbackQuery) -> None:
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "📍 <b>Joylashuvni o‘zgartirish</b>\n\n"
            "GPS orqali joylashuvingizni yuboring "
            "yoki shahar nomini yozing.",
            reply_markup=location_keyboard(),
        )


@router.callback_query(F.data == "settings:prayer_method")
async def choose_prayer_method(callback: CallbackQuery) -> None:
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "🕌 <b>Namoz hisoblash usulini tanlang</b>\n\n"
            "O‘zingiz foydalanadigan hisoblash usulini tanlang:",
            reply_markup=prayer_methods_menu(),
        )


@router.callback_query(F.data.startswith("settings:method:"))
async def save_prayer_method(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id

    try:
        method_id = int(callback.data.rsplit(":", 1)[1])

        if not 0 <= method_id <= 23:
            raise ValueError("Noto‘g‘ri hisoblash usuli")

        profile = get_user(user_id)

        if not profile:
            await callback.answer(
                "Avval /start buyrug‘ini yuboring.",
                show_alert=True,
            )
            return

        set_prayer_method(user_id, method_id)

        await callback.answer("Hisoblash usuli saqlandi!")

        if isinstance(callback.message, Message):
            await callback.message.answer(
                "✅ <b>Namoz hisoblash usuli saqlandi.</b>\n\n"
                f"Tanlangan usul raqami: <b>{method_id}</b>\n\n"
                "Yangi hisoblash usuli keyingi namoz vaqti "
                "so‘rovida qo‘llanadi.",
                reply_markup=settings_menu(),
            )

    except (ValueError, IndexError):
        await callback.answer(
            "Hisoblash usuli noto‘g‘ri.",
            show_alert=True,
        )

    except Exception:
        logger.exception("Namoz hisoblash usulini saqlashda xatolik.")
        await callback.answer(
            "Saqlashda xatolik yuz berdi.",
            show_alert=True,
        )


@router.callback_query(F.data == "settings:reminders")
async def show_reminders(callback: CallbackQuery) -> None:
    profile = get_user(callback.from_user.id)

    if not profile:
        await callback.answer(
            "Avval /start buyrug‘ini yuboring.",
            show_alert=True,
        )
        return

    enabled = bool(profile.get("reminders_enabled", True))

    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "🔔 <b>Kundalik eslatmalar</b>\n\n"
            "TAQVO BOT sizga har kuni:\n"
            "🌅 08:00 — Oxiratni eslatuvchi xabar\n"
            "🌙 20:00 — Kunlik eslatma yuboradi.\n\n"
            f"Holati: {'🟢 Yoqilgan' if enabled else '🔴 O‘chirilgan'}",
            reply_markup=reminders_menu(enabled),
        )


@router.callback_query(F.data.in_({
    "settings:reminders:on",
    "settings:reminders:off",
}))
async def toggle_reminders(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    enabled = callback.data.endswith(":on")

    try:
        profile = get_user(user_id)

        if not profile:
            await callback.answer(
                "Avval /start buyrug‘ini yuboring.",
                show_alert=True,
            )
            return

        set_reminders(user_id, enabled)

        await callback.answer(
            "Eslatmalar yoqildi!" if enabled else "Eslatmalar o‘chirildi!"
        )

        if isinstance(callback.message, Message):
            await callback.message.answer(
                "🔔 <b>Eslatmalar sozlamasi yangilandi.</b>\n\n"
                f"Holati: {'🟢 Yoqilgan' if enabled else '🔴 O‘chirilgan'}",
                reply_markup=reminders_menu(enabled),
            )

    except Exception:
        logger.exception("Eslatmalarni o‘zgartirishda xatolik.")
        await callback.answer(
            "Sozlamani o‘zgartirib bo‘lmadi.",
            show_alert=True,
        )
