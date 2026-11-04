"""TAQVO-BOT: aiogram 3 + aiohttp + SQLite. Python 3.11+"""
from __future__ import annotations

import asyncio
import logging
import os
import random
import sqlite3
import time
from contextlib import suppress
from pathlib import Path
from typing import Any

import aiohttp
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("taqvo")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL = os.getenv("CHANNEL_USERNAME", "@hakiymqalb").strip()
CHANNEL_URL = os.getenv(
    "CHANNEL_URL", "https://t.me/hakiymqalb"
).strip()
SITE_URL = os.getenv(
    "SITE_URL",
    "https://abdulhakiym.github.io/TAQVO-BOT/",
).strip()

CITY = os.getenv("CITY", "Karaganda").strip()
COUNTRY = os.getenv("COUNTRY", "Kazakhstan").strip()
METHOD = os.getenv("PRAYER_METHOD", "3").strip()
PORT = int(os.getenv("PORT", "10000"))
DB_PATH = os.getenv("DATABASE_PATH", "taqvo.sqlite3")

START = time.time()
HTTP: aiohttp.ClientSession | None = None

QUESTIONS = [
    (
        "Payg‘ambarimiz Muhammad ﷺ qayerda tavallud topganlar?",
        ["Makkada", "Madinada", "Toifda"],
        0,
        "U zot ﷺ Makkada tavallud topganlar.",
    ),
    (
        "Birinchi vahiy qaysi g‘orda nozil bo‘lgan?",
        ["Savr", "Hiro", "Uhud"],
        1,
        "Birinchi vahiy Hiro g‘orida nozil bo‘lgan.",
    ),
    (
        "Birinchi vahiy qaysi suraning oyatlari edi?",
        ["Fotiha", "Alaq", "Muddassir"],
        1,
        "Alaq surasining dastlabki oyatlari.",
    ),
    (
        "Hijrat qaysi shahardan qaysi shaharga bo‘lgan?",
        ["Makkadan Madinaga", "Madinadan Shomga", "Toifdan Makkaga"],
        0,
        "Musulmonlar Makkadan Madinaga hijrat qilganlar.",
    ),
    (
        "Payg‘ambarimiz ﷺ ning birinchi ayollari kim edilar?",
        ["Oisha", "Xadicha", "Hafsa"],
        1,
        "Xadicha رضي الله عنها.",
    ),
]


def db():
    con = sqlite3.connect(DB_PATH, timeout=20)
    con.row_factory = sqlite3.Row

    con.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL DEFAULT '',
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            score INTEGER NOT NULL DEFAULT 0,
            tasbeh INTEGER NOT NULL DEFAULT 0,
            updated_at INTEGER NOT NULL DEFAULT 0
        )
    """)
    con.commit()
    return con


def get_user(uid: int, name: str = "") -> dict[str, Any]:
    with db() as con:
        con.execute(
            """
            INSERT OR IGNORE INTO users
            (user_id, first_name, city, country, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (uid, name, CITY, COUNTRY, int(time.time())),
        )

        if name:
            con.execute(
                "UPDATE users SET first_name=?, updated_at=? WHERE user_id=?",
                (name, int(time.time()), uid),
            )

        row = con.execute(
            "SELECT * FROM users WHERE user_id=?",
            (uid,),
        ).fetchone()

        return dict(row)


def update_user(uid: int, **values):
    allowed = {
        "city",
        "country",
        "score",
        "tasbeh",
        "first_name",
    }

    fields = {
        key: value
        for key, value in values.items()
        if key in allowed
    }

    if not fields:
        return

    fields["updated_at"] = int(time.time())

    with db() as con:
        con.execute(
            "UPDATE users SET "
            + ", ".join(f"{key}=?" for key in fields)
            + " WHERE user_id=?",
            (*fields.values(), uid),
        )


def subscribed_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url=CHANNEL_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="sub:check",
                )
            ],
        ]
    )


def menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🕌 Namoz vaqtlarim"
                )
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Namoz vaqtlarini ko‘rish",
    )


def app_keyboard():
    if SITE_URL.startswith("https://"):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🌿 TAQVO PRO MAX ilovasini ochish",
                        web_app=WebAppInfo(url=SITE_URL),
                    )
                ]
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌿 TAQVO PRO MAX",
                    url=SITE_URL,
                )
            ]
        ]
    )


async def is_subscribed(bot: Bot, uid: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL, uid)

        return (
            member.status in (
                "creator",
                "administrator",
                "member",
            )
            or (
                member.status == "restricted"
                and bool(getattr(member, "is_member", False))
            )
        )

    except TelegramAPIError as error:
        log.warning(
            "Kanal obunasini tekshirib bo‘lmadi: %s",
            error,
        )
        return False


async def ask_subscription(message: Message):
    await message.answer(
        "TAQVO xizmatlaridan foydalanish uchun "
        "avval @hakiymqalb kanaliga obuna bo‘ling, "
        "so‘ng tasdiqlang.",
        reply_markup=subscribed_keyboard(),
    )


async def send_welcome(target: Message, user):
    await target.answer(
        "Assalomu alaykum va rohmatullohi va barokatuh, "
        f"{user.first_name or 'aziz foydalanuvchi'}! 🌿\n\n"
        "TAQVO-BOT’ga xush kelibsiz.",
        reply_markup=menu_keyboard(),
    )

    await target.answer(
        "TAQVO PRO MAX ilovasini ochish:",
        reply_markup=app_keyboard(),
    )


async def prayer_times(city: str, country: str) -> str:
    if HTTP is None:
        return "Namoz vaqti xizmati hozir tayyor emas."

    url = "https://api.aladhan.com/v1/timingsByCity"

    try:
        async with HTTP.get(
            url,
            params={
                "city": city,
                "country": country,
                "method": METHOD,
            },
        ) as response:
            response.raise_for_status()
            payload = await response.json()

        if payload.get("code") != 200:
            raise ValueError("API javobi noto‘g‘ri")

        data = payload["data"]
        timings = data["timings"]
        date = data.get("date", {}).get("readable", "")

        return (
            f"🕌 <b>Namoz vaqtlari</b>\n"
            f"📍 {city}, {country}\n"
            f"📅 {date}\n\n"
            f"🌅 Bomdod: <b>{timings['Fajr']}</b>\n"
            f"☀️ Quyosh: <b>{timings['Sunrise']}</b>\n"
            f"🕛 Peshin: <b>{timings['Dhuhr']}</b>\n"
            f"🌤 Asr: <b>{timings['Asr']}</b>\n"
            f"🌇 Shom: <b>{timings['Maghrib']}</b>\n"
            f"🌙 Xufton: <b>{timings['Isha']}</b>\n\n"
            "<i>Hisoblangan vaqtlarni mahalliy masjid "
            "taqvimi bilan solishtiring.</i>"
        )

    except (
        aiohttp.ClientError,
        KeyError,
        ValueError,
        TypeError,
    ) as error:
        log.warning("Prayer API: %s", error)
        return (
            "Namoz vaqtlarini olib bo‘lmadi. "
            "Keyinroq qayta urinib ko‘ring."
        )


async def start(message: Message, bot: Bot):
    if not message.from_user:
        return

    get_user(
        message.from_user.id,
        message.from_user.first_name or "",
    )

    if not await is_subscribed(bot, message.from_user.id):
        return await ask_subscription(message)

    await send_welcome(message, message.from_user)


async def check_subscription(
    call: CallbackQuery,
    bot: Bot,
):
    if not call.from_user:
        return await call.answer()

    if await is_subscribed(bot, call.from_user.id):
        await call.answer("Obuna tasdiqlandi!")
        await send_welcome(call.message, call.from_user)
    else:
        await call.answer(
            "Kanalga obuna bo‘ling, keyin qayta tekshiring.",
            show_alert=True,
        )


async def text_handler(message: Message, bot: Bot):
    if not message.from_user or not message.text:
        return

    if not await is_subscribed(bot, message.from_user.id):
        return await ask_subscription(message)

    user = get_user(
        message.from_user.id,
        message.from_user.first_name or "",
    )

    text = message.text.strip()

    if text == "🕌 Namoz vaqtlarim":
        await message.answer(
            await prayer_times(user["city"], user["country"])
        )

    elif text.startswith("/city"):
        parts = text.split(maxsplit=2)

        if len(parts) < 3:
            return await message.answer(
                "Shaharni quyidagicha yuboring:\n"
                "/city Karaganda Kazakhstan"
            )

        update_user(
            message.from_user.id,
            city=parts[1],
            country=parts[2],
        )

        await message.answer(
            f"Joylashuv saqlandi: {parts[1]}, {parts[2]}\n\n"
            + await prayer_times(parts[1], parts[2]),
            reply_markup=menu_keyboard(),
        )

    else:
        await message.answer(
            "Namoz vaqtlarini ko‘rish uchun pastdagi "
            "🕌 Namoz vaqtlarim tugmasini bosing.\n\n"
            "Shaharni almashtirish: "
            "/city Karaganda Kazakhstan",
            reply_markup=menu_keyboard(),
        )


async def health(request: web.Request):
    return web.json_response({
        "ok": True,
        "service": "TAQVO-BOT",
        "uptime": int(time.time() - START),
    })


async def main():
    global HTTP

    if not BOT_TOKEN:
        raise RuntimeError(
            "Render Environment Variables ichiga BOT_TOKEN kiriting."
        )

    db().close()

    HTTP = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=20)
    )

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
    )

    dp = Dispatcher()

    dp.message.register(start, CommandStart())
    dp.callback_query.register(
        check_subscription,
        F.data == "sub:check",
    )
    dp.message.register(text_handler, F.text)

    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/health", health)

    runner = web.AppRunner(app)

    try:
        await runner.setup()

        await web.TCPSite(
            runner,
            "0.0.0.0",
            PORT,
        ).start()

        await bot.delete_webhook(drop_pending_updates=True)

        log.info(
            "TAQVO-BOT ishga tushdi, port=%s",
            PORT,
        )

        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        await runner.cleanup()

        if HTTP and not HTTP.closed:
            await HTTP.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
