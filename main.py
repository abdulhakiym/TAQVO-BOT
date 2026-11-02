"""TAQVO BOT — /start -> kanalga obuna -> Mini App; qolgan hamma savolga AI javob beradi.
Ishga tushirish: python main.py  (Render: Background Worker)
Muhit o'zgaruvchilari: BOT_TOKEN, ANTHROPIC_API_KEY (majburiy);
CHANNEL, WEBAPP_URL, AI_MODEL (ixtiyoriy).
Botni kanalga ADMIN qilib qo'shing, aks holda obunani tekshirib bo'lmaydi.
"""
import asyncio
import logging
import os
from collections import defaultdict, deque

import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, WebAppInfo)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("taqvo")

BOT_TOKEN = os.environ["BOT_TOKEN"]
AI_KEY = os.environ["ANTHROPIC_API_KEY"]
CHANNEL = os.getenv("CHANNEL", "@hakiymqalb")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://abdulhakiym.github.io/TAQVO-BOT/")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-5-5")

SYSTEM = """Sen TAQVO AI — TAQVO BOT ning aqlli yordamchisisan.
- Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob ber (odatda o'zbek, lotin yozuvi).
- Har qanday savolga mos, aniq va foydali javob ber; javob uzunligini savolga moslashtir (oddiy savolga qisqa).
- Islomiy savollarda: Qur'on oyatlari va sahih hadislarni faqat aniq bilganingdagina keltir, manbani ayt.
  Hech qachon oyat, hadis yoki manba to'qima. Ishonching komil bo'lmasa, buni ochiq ayt.
- Ulamolar ixtilof qilgan masalada ixtilofni va mazhablar qarashlarini ko'rsat. Murakkab fatvo masalalarida
  qat'iy fatvo berma, ishonchli olim yoki muftiylikka murojaat qilishni tavsiya qil.
- Xushmuomala, hurmatli, sodda til. Markdown belgilarini (*, #) ishlatma, oddiy matn yoz."""

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
history: dict[int, deque] = defaultdict(lambda: deque(maxlen=12))
locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)


async def is_subscribed(user_id: int):
    """True / False; None — tekshirib bo'lmadi (masalan, bot kanalda admin emas)."""
    try:
        m = await bot.get_chat_member(CHANNEL, user_id)
        return m.status in ("member", "administrator", "creator") or (
            m.status == "restricted" and getattr(m, "is_member", False))
    except TelegramAPIError as e:
        log.error("getChatMember xatosi: %s", e)
        return None


def subscribe_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL.lstrip('@')}")],
        [InlineKeyboardButton(text="Obunani tekshirish", callback_data="check")],
    ])


def app_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="TAQVO PRO MAX ni ochish", web_app=WebAppInfo(url=WEBAPP_URL))],
    ])


SUBSCRIBE_TEXT = ("Botdan foydalanish uchun avval kanalimizga obuna bo‘ling, "
                  "so‘ng “Obunani tekshirish” tugmasini bosing.")
APP_TEXT = "Obuna tasdiqlandi. Ilovani ochish uchun tugmani bosing. Savolingiz bo‘lsa, shu yerga yozing."
CANT_CHECK = "Hozir obunani tekshirib bo‘lmadi. Birozdan so‘ng qayta urinib ko‘ring."


@dp.message(CommandStart())
async def start(m: Message):
    name = m.from_user.first_name or "aziz do‘st"
    await m.answer(f"Assalamu alaykum va rohmatulloh, {name}!")
    sub = await is_subscribed(m.from_user.id)
    if sub is None:
        await m.answer(CANT_CHECK)
    elif sub:
        await m.answer(APP_TEXT, reply_markup=app_kb())
    else:
        await m.answer(SUBSCRIBE_TEXT, reply_markup=subscribe_kb())


@dp.callback_query(F.data == "check")
async def check(c: CallbackQuery):
    sub = await is_subscribed(c.from_user.id)
    if sub is None:
        await c.answer(CANT_CHECK, show_alert=True)
    elif sub:
        await c.answer()
        await c.message.edit_text(APP_TEXT, reply_markup=app_kb())
    else:
        await c.answer("Hali obuna bo‘lmagansiz. Avval kanalga obuna bo‘ling.", show_alert=True)


async def ask_ai(uid: int, text: str) -> str:
    h = history[uid]
    h.append({"role": "user", "content": text})
    try:
        async with httpx.AsyncClient(timeout=60) as cl:
            r = await cl.post(
                "https://api.anthropic.com/v1/messages",
                headers={"x-api-key": AI_KEY, "anthropic-version": "2023-06-01"},
                json={"model": AI_MODEL, "max_tokens": 1200, "system": SYSTEM, "messages": list(h)},
            )
            r.raise_for_status()
            answer = "".join(b.get("text", "") for b in r.json()["content"]).strip()
        if not answer:
            raise ValueError("bo'sh javob")
        h.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        log.error("AI xatosi: %s", e)
        h.pop()  # muvaffaqiyatsiz savolni tarixdan olib tashlaymiz
        return "Kechirasiz, hozir javob bera olmadim. Birozdan so‘ng qayta yozing."


@dp.message(F.text & ~F.text.startswith("/"))
async def chat(m: Message):
    sub = await is_subscribed(m.from_user.id)
    if sub is None:
        return await m.answer(CANT_CHECK)
    if not sub:
        return await m.answer(SUBSCRIBE_TEXT, reply_markup=subscribe_kb())
    async with locks[m.from_user.id]:
        await bot.send_chat_action(m.chat.id, ChatAction.TYPING)
        answer = await ask_ai(m.from_user.id, m.text)
    for i in range(0, len(answer), 4000):  # Telegram: 4096 belgi chegarasi
        await m.answer(answer[i:i + 4000])


@dp.message()
async def other(m: Message):
    await m.answer("Savolingizni matn ko‘rinishida yozing, javob beraman.")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands()  # ortiqcha menyu yo'q
    log.info("TAQVO BOT ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
