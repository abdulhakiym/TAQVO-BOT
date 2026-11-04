from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from database import (
    get_user,
    set_prayer_method,
    set_reminders,
)
from keyboards import (
    PRAYER_METHODS,
    location_keyboard,
    prayer_method_keyboard,
    reminder_keyboard,
)

logger = logging.getLogger(__name__)

router = Router(name="settings")


def settings_menu():
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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


async def show_settings(message: Message) -> None:
    await message.answer(
        "⚙️ <b>TAQVO PRO MAX — Sozlamalar</b>\n\n"
        "Quyidagi bo‘limlardan birini tanlang:",
        reply_markup=settings_menu(),
    )


@router.message(Command("settings"))
async def settings_command(message: Message) -> None:
    profile = get_user(message.from_user.id)

    if not profile:
        await message.answer("Avval /start buyrug‘ini bosing.")
        return

    await show_settings(message)


@router.callback_query(F.data == "settings:back")
async def settings_back(callback: CallbackQuery) -> None:
    await callback.answer()

    if isinstance(callback.message, Message):
        await show_settings(callback.message)


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
    profile = get_user(callback.from_user.id)

    if not profile:
        await callback.answer(
            "Avval /start buyrug‘ini bosing.",
            show_alert=True,
        )
        return

    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "🕌 <b>Namoz hisoblash usuli</b>\n\n"
            "O‘zingizga mos hisoblash usulini tanlang:",
            reply_markup=prayer_method_keyboard(),
        )


@router.callback_query(F.data.startswith("settings:method:"))
async def save_prayer_method_handler(
    callback: CallbackQuery,
) -> None:
    profile = get_user(callback.from_user.id)

    if not profile:
        await callback.answer(
            "Avval /start buyrug‘ini bosing.",
            show_alert=True,
        )
        return

    try:
        method_id = int((callback.data or "").split(":")[-1])

        method_names = dict(PRAYER_METHODS)

        if method_id not in method_names:
            await callback.answer(
                "Noto‘g‘ri hisoblash usuli.",
                show_alert=True,
            )
            return

        set_prayer_method(callback.from_user.id, method_id)

        selected_name = method_names[method_id]

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
        logger.exception("Namoz hisoblash usulini saqlashda xatolik.")

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

    enabled = bool(profile.get("reminders_enabled", False))

    await callback.answer()

    if isinstance(callback.message, Message):
        await callback.message.answer(
            "🔔 <b>Kunlik eslatmalar</b>\n\n"
            "🌅 Tonggi eslatma — 08:00\n"
            "🌙 Kechki eslatma — 20:00\n\n"
            "Vaqtlar saqlangan vaqt mintaqangiz bo‘yicha belgilanadi.\n\n"
            "Eslatmalar holatini tanlang:",
            reply_markup=reminder_keyboard(enabled),
        )


@router.callback_query(
    F.data.in_({
        "settings:reminders:on",
        "settings:reminders:off",
    })
)
async def toggle_reminders(callback: CallbackQuery) -> None:
    profile = get_user(callback.from_user.id)

    if not profile:
        await callback.answer(
            "Avval /start buyrug‘ini bosing.",
            show_alert=True,
        )
        return

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
        logger.exception("Eslatmalar sozlamasini saqlashda xatolik.")

        await callback.answer(
            "Sozlamani saqlab bo‘lmadi.",
            show_alert=True,
        )
