"""TAQVO BOT — obuna -> shahar tanlash -> Mini App; AI suhbat; namoz, zikr va oxirat eslatmalari.
Render: Background Worker, Start Command: python main.py
Muhit o'zgaruvchilari: BOT_TOKEN, ANTHROPIC_API_KEY, DATABASE_URL (majburiy);
CHANNEL, WEBAPP_URL, AI_MODEL (ixtiyoriy). Botni kanalga ADMIN qiling.
"""
import asyncio
import logging
import os
from collections import defaultdict, deque
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import asyncpg
import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError
from aiogram.filters import Command, CommandStart
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, WebAppInfo)

from content import (AKHIRAH, COUNTRIES, PRAYER_NAMES, ZIKR_EVENING, ZIKR_MORNING)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("taqvo")

BOT_TOKEN = os.environ["BOT_TOKEN"]
AI_KEY = os.environ["ANTHROPIC_API_KEY"]
DATABASE_URL = os.environ["DATABASE_URL"]
CHANNEL = os.getenv("CHANNEL", "@hakiymqalb")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://abdulhakiym.github.io/TAQVO-BOT/")
AI_MODEL = os.getenv("AI_MODEL", "claude-sonnet-5-5")
AKHIRAH_HOURS = (9, 21)        # mahalliy vaqt bilan kuniga 2 marta
ZIKR_M_DELAY = 30 * 60         # tonggi zikr: Bomdoddan 30 daqiqa keyin
ZIKR_E_DELAY = 20 * 60         # kechki zikr: Shomdan 20 daqiqa keyin
WINDOW = 10 * 60               # kechikib qolgan eslatma shu oynadan keyin yuborilmaydi

SYSTEM = """Sen TAQVO AI — TAQVO BOT ning aqlli yordamchisisan.
- Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob ber (odatda o'zbek, lotin yozuvi).
- Har qanday savolga mos, aniq va foydali javob ber; javob uzunligini savolga moslashtir.
- Islomiy savollarda: oyat va sahih hadislarni faqat aniq bilganingdagina keltir, manbani ayt.
  Hech qachon oyat, hadis yoki manba to'qima. Ishonching komil bo'lmasa, buni ochiq ayt.
- Ulamolar ixtilof qilgan masalada ixtilofni ko'rsat. Murakkab fatvo masalalarida qat'iy fatvo berma,
  ishonchli olim yoki muftiylikka murojaat qilishni tavsiya qil.
- Xushmuomala, sodda til. Markdown belgilarini (*, #) ishlatma."""

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
http: httpx.AsyncClient
pool: asyncpg.Pool
history: dict[int, deque] = defaultdict(lambda: deque(maxlen=12))
locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

# ---------------------------------------------------------------- obuna
async def is_subscribed(uid: int):
    try:
        m = await bot.get_chat_member(CHANNEL, uid)
        return m.status in ("member", "administrator", "creator") or (
            m.status == "restricted" and getattr(m, "is_member", False))
    except TelegramAPIError as e:
        log.error("getChatMember xatosi: %s", e)
        return None


def subscribe_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL.lstrip('@')}")],
        [InlineKeyboardButton(text="Obunani tekshirish", callback_data="check")]])


def app_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="TAQVO PRO MAX ni ochish", web_app=WebAppInfo(url=WEBAPP_URL))]])


def countries_kb():
    b = [InlineKeyboardButton(text=c[0], callback_data=f"c:{i}") for i, c in enumerate(COUNTRIES)]
    return InlineKeyboardMarkup(inline_keyboard=[b[i:i + 2] for i in range(0, len(b), 2)])


def cities_kb(ci: int):
    b = [InlineKeyboardButton(text=c[0], callback_data=f"s:{ci}:{j}") for j, c in enumerate(COUNTRIES[ci][4])]
    rows = [b[i:i + 3] for i in range(0, len(b), 3)]
    rows.append([InlineKeyboardButton(text="‹ Davlatlar", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


SUBSCRIBE_TEXT = "Botdan foydalanish uchun avval kanalimizga obuna bo‘ling, so‘ng “Obunani tekshirish” tugmasini bosing."
APP_TEXT = "Obuna tasdiqlandi. Ilovani ochish uchun tugmani bosing. Savolingiz bo‘lsa, shu yerga yozing."
ASK_COUNTRY = "Namoz vaqtlari va zikr eslatmalari to‘g‘ri vaqtda kelishi uchun qaysi davlatda yashaysiz?"
CANT_CHECK = "Hozir obunani tekshirib bo‘lmadi. Birozdan so‘ng qayta urinib ko‘ring."


async def onboard(uid: int, reply):
    """Obuna tasdiqlangandan keyin: shahar saqlangan bo'lsa ilova, bo'lmasa davlat tanlash."""
    city = await pool.fetchval("SELECT city FROM users WHERE id=$1", uid)
    if city:
        await reply(APP_TEXT, app_kb())
    else:
        await reply(ASK_COUNTRY, countries_kb())


@dp.message(CommandStart())
async def start(m: Message):
    uid = m.from_user.id
    await pool.execute("INSERT INTO users(id, first_name) VALUES($1,$2) "
                       "ON CONFLICT (id) DO UPDATE SET first_name=$2, enabled=TRUE", uid, m.from_user.first_name)
    await m.answer(f"Assalamu alaykum va rohmatulloh, {m.from_user.first_name or 'aziz do‘st'}!")
    sub = await is_subscribed(uid)
    if sub is None:
        await m.answer(CANT_CHECK)
    elif sub:
        await onboard(uid, lambda t, k: m.answer(t, reply_markup=k))
    else:
        await m.answer(SUBSCRIBE_TEXT, reply_markup=subscribe_kb())


@dp.message(Command("city"))
async def change_city(m: Message):
    sub = await is_subscribed(m.from_user.id)
    if sub:
        await m.answer(ASK_COUNTRY, reply_markup=countries_kb())
    else:
        await m.answer(SUBSCRIBE_TEXT if sub is False else CANT_CHECK, reply_markup=subscribe_kb() if sub is False else None)


@dp.callback_query(F.data == "check")
async def check(c: CallbackQuery):
    sub = await is_subscribed(c.from_user.id)
    if sub is None:
        await c.answer(CANT_CHECK, show_alert=True)
    elif sub:
        await c.answer()
        await pool.execute("INSERT INTO users(id, first_name) VALUES($1,$2) ON CONFLICT (id) DO NOTHING",
                           c.from_user.id, c.from_user.first_name)
        await onboard(c.from_user.id, lambda t, k: c.message.edit_text(t, reply_markup=k))
    else:
        await c.answer("Hali obuna bo‘lmagansiz. Avval kanalga obuna bo‘ling.", show_alert=True)


@dp.callback_query(F.data == "back")
async def back(c: CallbackQuery):
    await c.answer()
    await c.message.edit_text(ASK_COUNTRY, reply_markup=countries_kb())


@dp.callback_query(F.data.startswith("c:"))
async def pick_country(c: CallbackQuery):
    ci = int(c.data[2:])
    await c.answer()
    await c.message.edit_text(f"{COUNTRIES[ci][0]}: shaharingizni tanlang.", reply_markup=cities_kb(ci))


@dp.callback_query(F.data.startswith("s:"))
async def pick_city(c: CallbackQuery):
    if await is_subscribed(c.from_user.id) is not True:
        return await c.answer(CANT_CHECK, show_alert=True)
    _, ci, j = c.data.split(":")
    country = COUNTRIES[int(ci)]
    city = country[4][int(j)]
    try:
        _, tz = await fetch_timings(city[1], country[1], country[2], country[3])
    except Exception as e:
        log.error("Namoz vaqtlari xatosi: %s", e)
        return await c.answer("Hozir namoz vaqtlarini olib bo‘lmadi. Birozdan so‘ng qayta urinib ko‘ring.", show_alert=True)
    await pool.execute(
        "INSERT INTO users(id, first_name, country, country_uz, city, city_uz, method, school, tz, enabled) "
        "VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,TRUE) ON CONFLICT (id) DO UPDATE SET "
        "country=$3, country_uz=$4, city=$5, city_uz=$6, method=$7, school=$8, tz=$9, enabled=TRUE",
        c.from_user.id, c.from_user.first_name, country[1], country[0], city[1], city[0], country[2], country[3], tz)
    await c.answer()
    await c.message.edit_text(
        f"Tayyor: {city[0]}, {country[0]}.\nEndi namoz vaqtlari, tonggi va kechki zikr hamda oxirat eslatmalari "
        f"shu yerga keladi. Shaharni o‘zgartirish uchun /city yozing.", reply_markup=app_kb())

# ---------------------------------------------------------------- AI suhbat
async def ask_ai(uid: int, text: str) -> str:
    h = history[uid]
    h.append({"role": "user", "content": text})
    try:
        r = await http.post("https://api.anthropic.com/v1/messages",
                            headers={"x-api-key": AI_KEY, "anthropic-version": "2023-06-01"},
                            json={"model": AI_MODEL, "max_tokens": 1200, "system": SYSTEM, "messages": list(h)})
        r.raise_for_status()
        answer = "".join(b.get("text", "") for b in r.json()["content"]).strip()
        if not answer:
            raise ValueError("bo'sh javob")
        h.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        log.error("AI xatosi: %s", e)
        h.pop()
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
    for i in range(0, len(answer), 4000):
        await m.answer(answer[i:i + 4000])


@dp.message()
async def other(m: Message):
    await m.answer("Savolingizni matn ko‘rinishida yozing, javob beraman.")

# ---------------------------------------------------------------- namoz vaqtlari
TIMINGS: dict = {}


async def fetch_timings(city, country, method, school, date=None):
    url = "https://api.aladhan.com/v1/timingsByCity" + (f"/{date}" if date else "")
    r = await http.get(url, params={"city": city, "country": country, "method": method, "school": school})
    r.raise_for_status()
    d = r.json()["data"]
    return {k: str(v)[:5] for k, v in d["timings"].items()}, d["meta"]["timezone"]


def hm(s: str) -> int:
    h, m = s.split(":")
    return int(h) * 3600 + int(m) * 60

# ---------------------------------------------------------------- eslatma matnlari
AYAH_CACHE: dict = {}


async def ayah_text(ref: str) -> str:
    if ref not in AYAH_CACHE:
        r = await http.get(f"https://api.alquran.cloud/v1/ayah/{ref}/editions/quran-uthmani,uz.sodik")
        r.raise_for_status()
        ar, uz = r.json()["data"][0]["text"], r.json()["data"][1]["text"]
        AYAH_CACHE[ref] = f"{ar}\n\n{uz}\n\nQur’on, {ref}"
    return AYAH_CACHE[ref]


def pick(items: list, day, slot: int = 0):
    return items[(day.toordinal() * 2 + slot) % len(items)]


async def akhirah_message(day, slot: int) -> str:
    item = pick(AKHIRAH, day, slot)
    body = None
    if item["t"] == "q":
        try:
            body = await ayah_text(item["ref"])
        except Exception as e:
            log.error("Oyat olinmadi (%s): %s", item["ref"], e)
            item = next(i for i in AKHIRAH[day.toordinal() % len(AKHIRAH):] + AKHIRAH if i["t"] == "h")
    if body is None:
        body = f"{item['text']}\n\nManba: {item['src']}"
    return f"Oxirat eslatmasi\n\n{body}"


def zikr_message(items: list, day, title: str) -> str:
    z = pick(items, day)
    ar = f"\n\n{z['ar']}" if z["ar"] else ""
    return f"{title}\n\n{z['text']}{ar}\n\nManba: {z['src']}"


async def build_message(kind: str, u, t: dict, day) -> str:
    if kind.startswith("p_"):
        k = kind[2:]
        return f"{PRAYER_NAMES[k]} namozi vaqti kirdi ({u['city_uz']}, {t[k]}). Alloh qabul qilsin."
    if kind == "zikr_m":
        return zikr_message(ZIKR_MORNING, day, "Tonggi zikr vaqti. Bomdoddan keyin zikrni unutmang.")
    if kind == "zikr_e":
        return zikr_message(ZIKR_EVENING, day, "Kechki zikr vaqti. Shomdan keyin zikrni unutmang.")
    return await akhirah_message(day, 0 if kind == "ah_1" else 1)

# ---------------------------------------------------------------- rejalashtiruvchi
async def tick():
    users = await pool.fetch("SELECT * FROM users WHERE enabled AND city IS NOT NULL AND tz IS NOT NULL")
    now = datetime.now(timezone.utc)
    if len(TIMINGS) > 600:
        TIMINGS.clear()
    for u in users:
        loc = now.astimezone(ZoneInfo(u["tz"]))
        day, sec = loc.date(), loc.hour * 3600 + loc.minute * 60 + loc.second
        key = (u["city"], u["country"], u["method"], u["school"], day.isoformat())
        if key not in TIMINGS:
            try:
                TIMINGS[key] = (await fetch_timings(u["city"], u["country"], u["method"], u["school"],
                                                    day.strftime("%d-%m-%Y")))[0]
            except Exception as e:
                log.error("Vaqt olinmadi %s: %s", key, e)
                continue
        t = TIMINGS[key]
        events = [(f"p_{k}", hm(t[k])) for k in PRAYER_NAMES]
        events += [("zikr_m", hm(t["Fajr"]) + ZIKR_M_DELAY), ("zikr_e", hm(t["Maghrib"]) + ZIKR_E_DELAY),
                   ("ah_1", AKHIRAH_HOURS[0] * 3600), ("ah_2", AKHIRAH_HOURS[1] * 3600)]
        for kind, due in events:
            if not 0 <= sec - due < WINDOW:
                continue
            claimed = await pool.fetchval(
                "INSERT INTO sent(user_id, kind, day) VALUES($1,$2,$3) ON CONFLICT DO NOTHING RETURNING 1",
                u["id"], kind, day)
            if not claimed:
                continue  # allaqachon yuborilgan: takror yuborilmaydi
            try:
                await bot.send_message(u["id"], await build_message(kind, u, t, day))
            except TelegramForbiddenError:
                await pool.execute("UPDATE users SET enabled=FALSE WHERE id=$1", u["id"])
            except Exception as e:
                log.error("Yuborilmadi %s/%s: %s", u["id"], kind, e)
                await pool.execute("DELETE FROM sent WHERE user_id=$1 AND kind=$2 AND day=$3", u["id"], kind, day)
            await asyncio.sleep(0.05)  # Telegram tezlik chegarasi


async def scheduler():
    while True:
        try:
            await tick()
        except Exception as e:
            log.exception("Rejalashtiruvchi xatosi: %s", e)
        await asyncio.sleep(30)

# ---------------------------------------------------------------- ishga tushirish
async def main():
    global http, pool
    http = httpx.AsyncClient(timeout=60)
    pool = await asyncpg.create_pool(DATABASE_URL)
    await pool.execute("""CREATE TABLE IF NOT EXISTS users(
        id BIGINT PRIMARY KEY, first_name TEXT, country TEXT, country_uz TEXT, city TEXT, city_uz TEXT,
        method INT, school INT, tz TEXT, enabled BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now())""")
    await pool.execute("""CREATE TABLE IF NOT EXISTS sent(
        user_id BIGINT NOT NULL, kind TEXT NOT NULL, day DATE NOT NULL, PRIMARY KEY(user_id, kind, day))""")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands()
    asyncio.create_task(scheduler())
    log.info("TAQVO BOT ishga tushdi")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
