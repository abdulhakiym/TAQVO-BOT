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

from database import (
    get_user,
    set_prayer_method,
    set_reminders,
)
from keyboards import location_keyboard


logger = logging.getLogger(__name__)

router = Router(name="settings")


PRAYER_METHODS = [
    (0, "Shia Ithna-Ashari"),
    (1, "University of Islamic Sciences, Karachi"),
    (2, "Islamic Society of North America"),
    (3, "Muslim World League"),
    (4, "Umm Al-Qura University, Makkah"),
    (5, "Egyptian General Authority of Survey"),
    (7, "Institute of Geophysics, University of Tehran"),
    (8, "Gulf Region"),
    (9, "Kuwait"),
    (10, "Qatar"),
    (11, "Majlis Ugama Islam Singapura"),
    (12, "Union Organization Islamic de France"),
    (13, "Diyanet İşleri Başkanlığı, Turkey"),
    (14, "Spiritual Administration of Muslims of Russia"),
    (15, "Moonsighting Committee Worldwide"),
    (16, "Dubai"),
    (17, "Jabatan Kemajuan Islam Malaysia"),
    (18, "Tunisia"),
    (19, "Algeria"),
    (20, "Kementerian Agama Indonesia"),
    (21, "Morocco"),
    (22, "Comunidade Islamica de Lisboa"),
    (23, "Ministry of Awqaf, Jordan"),
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
            text="⬅️ Orqaga",
            callback_data="settings:back",
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def reminders_menu(enabled: bool) -> InlineKeyboardMarkup:
    status = "🟢 Yoqilgan" if enabled else "🔴 O‘chirilgan"

    buttons = [
        [
            InlineKeyboardButton(
                text=f"Holati: {status}",
                callback_data="settings:reminders:status",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔔 Eslatmalarni yoqish",
                callback_data="settings:reminders:on",
            )
        ],
        [
            InlineKeyboardButton(
                text="🔕 Eslatmalarni o‘chirish",
                callback_data="settings:reminders:off",
            )
        ],
        [
            InlineKeyboardButton(
                text="⬅️ Orqaga",
                callback_data="settings:back",
            )
        ],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


@router.message(Command("settings"))
async def settings_command(message: Message) -> None:
    await message.answer(
        "⚙️ <b>TAQVO PRO MAX — Sozlamalar</b>\n\n"
        "Quyidagi bo‘limlardan birini tanlang:",
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
            "Yangi joylashuvingizni GPS orqali yuboring "
            "yoki shahar nomini yozing.",
            reply_markup=location_keyboard(),
        )


@router.callback_query(F.data == "settings:prayer_method")
async def select_prayer_method(callback: CallbackQuery) -> None:
    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "🕌 <b>Namoz hisoblash usuli</b>\n\n"
            "O‘zingizga mos hisoblash usulini tanlang:",
            reply_markup=prayer_methods_menu(),
        )


@router.callback_query(F.data.startswith("settings:method:"))
async def save_prayer_method(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id

    try:
        method_id = int((callback.data or "").split(":")[-1])

        valid_methods = {
            method_id
            for method_id, _ in PRAYER_METHODS
        }

        if method_id not in valid_methods:
            await callback.answer(
                "Noto‘g‘ri hisoblash usuli.",
                show_alert=True,
            )
            return

        set_prayer_method(user_id, method_id)

        selected_name = next(
            name
            for method, name in PRAYER_METHODS
            if method == method_id
        )

        await callback.answer("Hisoblash usuli saqlandi!")

        if isinstance(callback.message, Message):
            await callback.message.answer(
                "✅ <b>Namoz hisoblash usuli saqlandi.</b>\n\n"
                f"Tanlangan usul: <b>{selected_name}</b>\n\n"
                "Yangi usul keyingi namoz vaqtlari hisobida qo‘llanadi."
            )

    except (ValueError, TypeError):
        await callback.answer(
            "Hisoblash usulini tanlashda xatolik.",
            show_alert=True,
        )

    except Exception:
        logger.exception("Namoz usulini saqlashda xatolik.")
        await callback.answer(
            "Sozlamani saqlab bo‘lmadi.",
            show_alert=True,
        )


@router.callback_query(F.data == "settings:reminders")
async def show_reminders(callback: CallbackQuery) -> None:
    profile = get_user(callback.from_user.id)

    if not profile:
        await callback.answer(
            "Avval /start buyrug‘ini bosing.",
            show_alert=True,
        )
        return

    enabled = bool(profile.get("reminders_enabled", True))

    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "🔔 <b>Kunlik eslatmalar</b>\n\n"
            "Eslatmalar vaqti:\n"
            "🌅 Tonggi eslatma — 08:00\n"
            "🌙 Kechki eslatma — 20:00\n\n"
            "Vaqtlar sizning saqlangan vaqt mintaqangiz bo‘yicha belgilanadi.\n\n"
            "Holatni tanlang:",
            reply_markup=reminders_menu(enabled),
        )


@router.callback_query(F.data == "settings:reminders:status")
async def reminder_status(callback: CallbackQuery) -> None:
    profile = get_user(callback.from_user.id)

    if not profile:
        await callback.answer(
            "Foydalanuvchi ma’lumotlari topilmadi.",
            show_alert=True,
        )
        return

    enabled = bool(profile.get("reminders_enabled", True))

    status = "yoqilgan" if enabled else "o‘chirilgan"

    await callback.answer(
        f"Eslatmalar hozir {status}.",
        show_alert=True,
    )


@router.callback_query(F.data.in_({
    "settings:reminders:on",
    "settings:reminders:off",
}))
async def toggle_reminders(callback: CallbackQuery) -> None:
    enabled = callback.data == "settings:reminders:on"

    try:
        set_reminders(callback.from_user.id, enabled)

        await callback.answer(
            "Eslatmalar yoqildi!" if enabled else "Eslatmalar o‘chirildi!"
        )

        if isinstance(callback.message, Message):
            await callback.message.answer(
                (
                    "✅ <b>Kunlik eslatmalar yoqildi.</b>\n\n"
                    "🌅 08:00 — Tonggi eslatma\n"
                    "🌙 20:00 — Kechki eslatma"
                )
                if enabled
                else
                "🔕 <b>Kunlik eslatmalar o‘chirildi.</b>\n\n"
                "Endi sizga rejalashtirilgan eslatmalar yuborilmaydi."
            )

    except Exception:
        logger.exception("Eslatmalar sozlamasida xatolik.")
        await callback.answer(
            "Sozlamani saqlab bo‘lmadi.",
            show_alert=True,
        )
