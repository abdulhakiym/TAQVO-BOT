# -*- coding: utf-8 -*-
"""
TAQVO PRO MAX — islomiy Telegram bot (main.py) — to'liq versiya
Kutubxonalar: aiogram 3.x, aiohttp, tzdata
"""
import asyncio
import hashlib
import hmac
import html
import itertools
import json
import logging
import os
import random
import sqlite3
import time
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qsl
from zoneinfo import ZoneInfo

import aiohttp
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatAction, ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import BotCommand, MenuButtonWebApp, Message, WebAppInfo

# ====================== SOZLAMALAR ======================
BOT_TOKEN = os.getenv("BOT_TOKEN", "BU_YERGA_BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL", "@kanal_username")
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://USERNAME.github.io/REPO/")
AI_KEYS = [k.strip() for k in os.getenv("AI_KEYS", "").split(",") if k.strip()]
AI_MODEL = os.getenv("AI_MODEL", "claude-haiku-5-5")
DB_PATH = os.getenv("DB_PATH", "taqvo.db")
PORT = int(os.getenv("PORT", "8080"))
CHANNEL_LINK = "https://t.me/" + CHANNEL.lstrip("@")

MORNING_ZIKR_TIME = (8, 0)
EVENING_ZIKR_TIME = (20, 0)
DEATH_TIMES = [(10, 30), (22, 0)]
AI_CONCURRENCY = 200
DAILY_CAP = 400  # saytda kuniga olish mumkin bo'lgan maksimal ball

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("taqvo")
esc = html.escape

bot: Bot = None
session: aiohttp.ClientSession = None
dp = Dispatcher()

# ====================== BAZA ======================
db = sqlite3.connect(DB_PATH, check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY, name TEXT,
    city TEXT DEFAULT 'Toshkent', lat REAL DEFAULT 41.3111, lon REAL DEFAULT 69.2797,
    tz TEXT DEFAULT 'Asia/Tashkent', subscribed INTEGER DEFAULT 0, blocked INTEGER DEFAULT 0)""")
db.execute("CREATE TABLE IF NOT EXISTS sent(uid INTEGER, key TEXT, PRIMARY KEY(uid,key))")
db.execute("""CREATE TABLE IF NOT EXISTS scores(
    uid INTEGER PRIMARY KEY, name TEXT, uname TEXT, photo TEXT,
    score INTEGER DEFAULT 0, tasbeh INTEGER DEFAULT 0, last INTEGER DEFAULT 0,
    day TEXT DEFAULT '', gain INTEGER DEFAULT 0)""")
db.commit()


def upsert_user(uid, name):
    db.execute("INSERT OR IGNORE INTO users(id,name) VALUES(?,?)", (uid, name))
    db.execute("UPDATE users SET name=?, blocked=0 WHERE id=?", (name, uid))
    db.commit()


def get_user(uid):
    return db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()


def set_sub(uid, v):
    db.execute("UPDATE users SET subscribed=? WHERE id=?", (v, uid))
    db.commit()


def was_sent(uid, key):
    return db.execute("SELECT 1 FROM sent WHERE uid=? AND key=?", (uid, key)).fetchone() is not None


def mark_sent(uid, key):
    db.execute("INSERT OR IGNORE INTO sent VALUES(?,?)", (uid, key))
    db.commit()


# ====================== SHAHARLAR ======================
CITIES = {
    "toshkent": ("Toshkent", 41.3111, 69.2797), "tashkent": ("Toshkent", 41.3111, 69.2797),
    "samarqand": ("Samarqand", 39.6542, 66.9597), "buxoro": ("Buxoro", 39.7747, 64.4286),
    "andijon": ("Andijon", 40.7821, 72.3442), "namangan": ("Namangan", 41.0011, 71.6683),
    "fargona": ("Farg'ona", 40.3842, 71.7843), "qoqon": ("Qo'qon", 40.5286, 70.9425),
    "margilon": ("Marg'ilon", 40.4711, 71.7246), "urganch": ("Urganch", 41.5506, 60.6317),
    "xiva": ("Xiva", 41.3783, 60.3639), "nukus": ("Nukus", 42.4600, 59.6100),
    "qarshi": ("Qarshi", 38.8606, 65.7891), "termiz": ("Termiz", 37.2242, 67.2783),
    "navoiy": ("Navoiy", 40.0844, 65.3792), "jizzax": ("Jizzax", 40.1158, 67.8422),
    "guliston": ("Guliston", 40.4897, 68.7842), "angren": ("Angren", 41.0167, 70.1436),
    "chirchiq": ("Chirchiq", 41.4689, 69.5822), "olmaliq": ("Olmaliq", 40.8444, 69.5984),
    "shahrisabz": ("Shahrisabz", 39.0578, 66.8342), "denov": ("Denov", 38.2689, 67.8997),
}


def norm(s: str) -> str:
    s = s.lower().strip()
    for ch in "'ʻʼ’`‘ ":
        s = s.replace(ch, "")
    return s


# ====================== NAMOZ VAQTLARI (internetdan) ======================
_tcache = {}


async def get_timings(lat, lon, date_str):
    key = (round(lat, 2), round(lon, 2), date_str)
    if key in _tcache:
        return _tcache[key]
    if len(_tcache) > 3000:
        _tcache.clear()
    url = f"https://api.aladhan.com/v1/timings/{date_str}"
    params = {"latitude": lat, "longitude": lon, "method": 3, "school": 1}
    for _ in range(3):
        try:
            async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as r:
                d = await r.json()
            t = d["data"]["timings"]
            res = {k: t[k][:5] for k in ("Fajr", "Dhuhr", "Asr", "Maghrib", "Isha")}
            res["tz"] = d["data"]["meta"]["timezone"]
            _tcache[key] = res
            return res
        except Exception as e:
            log.warning("Namoz vaqti xato: %s", e)
            await asyncio.sleep(2)
    return None


async def geocode(name):
    try:
        async with session.get("https://geocoding-api.open-meteo.com/v1/search",
                               params={"name": name, "count": 1, "language": "en", "format": "json"},
                               timeout=aiohttp.ClientTimeout(total=15)) as r:
            d = await r.json()
        x = d["results"][0]
        return x["name"], x["latitude"], x["longitude"], x.get("timezone")
    except Exception:
        return None


def times_text(city, t):
    return (f"📍 <b>{esc(city)}</b> uchun bugungi namoz vaqtlari:\n\n"
            f"🌅 Bomdod — <b>{t['Fajr']}</b>\n☀️ Peshin — <b>{t['Dhuhr']}</b>\n"
            f"🌤 Asr — <b>{t['Asr']}</b>\n🌇 Shom — <b>{t['Maghrib']}</b>\n🌙 Xufton — <b>{t['Isha']}</b>")


async def apply_location(m: Message, city, lat, lon, tz=None):
    use_tz = tz or "Asia/Tashkent"
    try:
        date_str = datetime.now(ZoneInfo(use_tz)).strftime("%d-%m-%Y")
    except Exception:
        use_tz = "Asia/Tashkent"
        date_str = datetime.now(ZoneInfo(use_tz)).strftime("%d-%m-%Y")
    t = await get_timings(lat, lon, date_str)
    if not t:
        await m.answer("Namoz vaqtlarini hozir olib bo'lmadi. Birozdan so'ng qayta urinib ko'ring.")
        return
    use_tz = tz or t["tz"]
    db.execute("UPDATE users SET city=?,lat=?,lon=?,tz=? WHERE id=?", (city, lat, lon, use_tz, m.from_user.id))
    db.commit()
    await m.answer(times_text(city, t) + "\n\nNamoz vaqti kirganda sizga shu joy vaqti bilan eslatib turaman. "
                                         "Boshqa joyga o'tsangiz, shahar nomini yozing yoki lokatsiya yuboring.")


# ====================== HADIS VA OYATLAR ======================
PRAYERS = [("Fajr", "Bomdod"), ("Dhuhr", "Peshin"), ("Asr", "Asr"), ("Maghrib", "Shom"), ("Isha", "Xufton")]

PRAYER_QUOTES = {
    "Bomdod": [
        "📖 Rasululloh ﷺ: «Kim bomdod namozini o'qisa, u Allohning himoyasida bo'ladi.» (Muslim)",
        "📖 Rasululloh ﷺ: «Bomdodning ikki rakat sunnati dunyo va undagi barcha narsadan yaxshiroqdir.» (Muslim)",
        "📖 Qur'on (Isro, 78): «Bomdod namozini ham (o'qing). Albatta, bomdod namozi (farishtalar tomonidan) guvoh bo'lingandir.»",
    ],
    "Peshin": [
        "📖 Qur'on (Niso, 103): «Albatta, namoz mo'minlarga vaqti belgilangan farz qilingandir.»",
        "📖 Abdulloh ibn Mas'ud r.a.: «Allohga eng suyukli amal qaysi?» — Rasululloh ﷺ: «O'z vaqtida o'qilgan namoz.» (Buxoriy, Muslim)",
        "📖 Rasululloh ﷺ: «Biringizning eshigi oldida daryo oqib tursa va u har kuni besh marta yuvinsa, kiridan asar qolarmidi?» "
        "Sahobalar: «Yo'q». «Besh vaqt namoz ham shunday — Alloh u bilan xatolarni yuvadi.» (Buxoriy, Muslim)",
    ],
    "Asr": [
        "📖 Qur'on (Baqara, 238): «Namozlarni va (ayniqsa) o'rtadagi namozni saqlangiz.»",
        "📖 Rasululloh ﷺ: «Kimning asr namozi o'tib ketsa, go'yo oilasi va mol-mulkidan ayrilgandek bo'ladi.» (Buxoriy, Muslim)",
    ],
    "Shom": [
        "📖 Qur'on (Hud, 114): «Kunning ikki chetida va tunning (kunga) yaqin qismlarida namoz o'qing. Albatta, yaxshiliklar yomonliklarni ketkazadi.»",
        "📖 Rasululloh ﷺ: «Besh vaqt namoz o'rtasidagi gunohlarga kafforatdir, agar katta gunohlardan saqlansa.» (Muslim)",
    ],
    "Xufton": [
        "📖 Rasululloh ﷺ: «Kim xuftonni jamoat bilan o'qisa, tunning yarmini ibodat bilan o'tkazgandek bo'ladi.» (Muslim)",
        "📖 Rasululloh ﷺ: «Munofiqlarga eng og'ir namoz — xufton va bomdoddir. Agar ularda qancha ajr borligini bilsalar, emaklab bo'lsa ham kelardilar.» (Buxoriy, Muslim)",
    ],
}

DEATH_QUOTES = [
    "📖 Rasululloh ﷺ: «Lazzatlarni uzuvchi narsa — o'limni ko'p eslanglar.» (Termiziy, Nasoiy, Ibn Moja)",
    "📖 Qur'on (Oli Imron, 185): «Har bir jon o'limni totuvchidir. Qiyomat kuni ish haqlaringiz to'liq beriladi. Kim do'zaxdan uzoqlashtirilib, jannatga kiritilsa, albatta u yutuqqa erishibdi. Dunyo hayoti esa aldovchi matodan boshqa narsa emas.»",
    "📖 Rasululloh ﷺ: «Dunyoda go'yo musofir yoki yo'lovchidek bo'l.» (Buxoriy)",
    "📖 Rasululloh ﷺ: «Inson vafot etsa, amali uzilib qoladi — uch narsadan tashqari: sadaqai joriya, foydali ilm va o'zi uchun duo qiladigan solih farzand.» (Muslim)",
    "📖 Qur'on (Jum'a, 8): «Albatta, sizlar qochayotgan o'lim, u sizga yetib kelguvchidir.»",
    "📖 Qur'on (Zalzala, 7-8): «Kim zarra miqdorida yaxshilik qilsa, uni ko'radi. Kim zarra miqdorida yomonlik qilsa, uni ko'radi.»",
    "📖 Rasululloh ﷺ: «Besh narsani besh narsadan oldin g'animat bil: qarilikdan oldin yoshlikni, kasallikdan oldin sog'liqni, kambag'allikdan oldin boylikni, mashg'ullikdan oldin bo'sh vaqtni va o'limdan oldin hayotni.» (Hokim, sahih)",
    "📖 Qur'on (Anbiyo, 35): «Har bir jon o'limni totuvchidir. Sizlarni imtihon uchun yaxshilik ham, yomonlik ham bilan sinaymiz va Bizga qaytarilasizlar.»",
    "📖 Rasululloh ﷺ: «Qabr — oxirat manzillarining birinchisidir. Kim undan najot topsa, keyingilari osonroq bo'ladi.» (Termiziy, Ibn Moja — hasan)",
    "📖 Qur'on (Ankabut, 57): «Har bir jon o'limni totuvchidir. So'ngra Bizga qaytarilasizlar.»",
]


def prayer_text(name, uz, city, hhmm):
    return (f"🕌 <b>{uz} namozi vaqti bo'ldi</b>\n📍 {esc(city)} · {hhmm}\n\n{random.choice(PRAYER_QUOTES[uz])}\n\n"
            f"Alloh namozingizni qabul qilsin, {esc(name)}.\n"
            f"📱 Zikr, Qur'on va boshqa bo'limlarni chap burchakdagi <b>Menyu</b>dan o'qishingiz mumkin.")


SAYYID = ("اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ خَلَقْتَنِي وَأَنَا عَبْدُكَ وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ "
          "أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ وَأَبُوءُ لَكَ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ")


def morning_text(name):
    return (f"🌅 <b>Ertalabki zikr vaqti</b>\n\n{esc(name)}, kunni Alloh zikri bilan boshlang:\n\n"
            "1️⃣ Oyatul Kursiy (Baqara, 255) — 1 marta\n"
            "2️⃣ Ixlos, Falaq va Nos suralari — 3 martadan\n"
            "3️⃣ «Subhanallohi va bihamdih» (سُبْحَانَ اللَّهِ وَبِحَمْدِهِ) — 100 marta\n"
            "📖 Rasululloh ﷺ: «Kim kuniga 100 marta shuni aytsa, xatolari dengiz ko'pigicha bo'lsa ham kechiriladi.» (Buxoriy, Muslim)\n\n"
            f"4️⃣ Sayyidul istig'for:\n<i>{SAYYID}</i>\n"
            "📖 «Kim uni ishonch bilan ertalab aytib, o'sha kuni kechgacha vafot etsa, jannat ahlidan bo'ladi.» (Buxoriy)\n\n"
            "📱 Zikrlar to'liq matni chap burchakdagi <b>Menyu</b>da.")


def evening_text(name):
    return (f"🌙 <b>Kechki zikr vaqti</b>\n\n{esc(name)}, kunni Alloh zikri bilan yakunlang:\n\n"
            "1️⃣ Oyatul Kursiy (Baqara, 255) — 1 marta\n"
            "2️⃣ Ixlos, Falaq va Nos suralari — 3 martadan\n"
            "3️⃣ أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ — 3 marta (Muslim)\n"
            f"4️⃣ Sayyidul istig'for:\n<i>{SAYYID}</i>\n"
            "📖 «Kim uni ishonch bilan kechqurun aytib, tong otguncha vafot etsa, jannat ahlidan bo'ladi.» (Buxoriy)\n\n"
            "📱 Zikrlar to'liq matni chap burchakdagi <b>Menyu</b>da.")


def death_text(name):
    return (f"⏳ <b>O'lim va oxiratni eslang</b>\n\n{random.choice(DEATH_QUOTES)}\n\n"
            f"{esc(name)}, bugun oxirat uchun nima tayyorladingiz? Alloh husni xotima nasib qilsin.")


# ====================== OBUNA TEKSHIRUVI ======================
_sub_cache = {}


async def is_sub(uid, fresh=False):
    c = _sub_cache.get(uid)
    if c and not fresh and time.time() - c < 300:
        return True
    ok = False
    try:
        mem = await bot.get_chat_member(CHANNEL, uid)
        ok = mem.status in ("member", "administrator", "creator") or \
            (mem.status == "restricted" and getattr(mem, "is_member", False))
    except Exception as e:
        log.warning("Obuna tekshiruvi xato (bot kanalda admin ekanini tekshiring): %s", e)
    if ok:
        _sub_cache[uid] = time.time()
    else:
        _sub_cache.pop(uid, None)
    return ok


def greet(name):
    return (f"Assalamu alaykum va rohmatulloh, <b>{esc(name)}</b>! 🌙\n"
            "Botimizga xush kelibsiz. Alloh iymoningizni salomat qilsin va amallaringizni qabul qilsin.\n\n")


def welcome_text(name):
    return (greet(name) + "✅ Kanalimizga obuna bo'lganingiz tasdiqlandi. Jazakallohu xayran!\n\n"
            f"🌐 Bizning saytimiz (islomiy mini ilova): {MINI_APP_URL}\n"
            "yoki chap burchakdagi <b>Menyu</b> orqali oching.\n\n"
            "📍 Namoz vaqtlari to'g'ri kelishi uchun <b>shahringiz nomini yozing</b> (masalan: Samarqand) "
            "yoki lokatsiyangizni yuboring. Aks holda Toshkent vaqti bilan eslatib turaman.\n\n"
            "Savolingiz bo'lsa, shunchaki yozing — javob beraman.")


def ask_sub_text(name):
    return (greet(name) + "Kanalimizga obuna bo'lganmisiz? Hozircha obunangiz topilmadi.\n\n"
            f"👉 Obuna bo'ling: {CHANNEL_LINK}\n\n"
            "Obuna bo'lgach, istalgan xabar yozing (yoki /start) — men avtomatik tekshirib tasdiqlayman.")


async def gate(m: Message) -> bool:
    uid = m.from_user.id
    name = m.from_user.first_name or "aziz do'st"
    upsert_user(uid, name)
    row = get_user(uid)
    if await is_sub(uid):
        if not row["subscribed"]:
            set_sub(uid, 1)
            await m.answer(welcome_text(name))
            return False
        return True
    set_sub(uid, 0)
    await m.answer(ask_sub_text(name))
    return False


# ====================== SUNIY INTELLEKT ======================
SYSTEM = """Sen islomiy Telegram botning yordamchisisan. Ahli sunna val jamoa yo'lida, odobli, samimiy va ravshan javob ber.
Foydalanuvchi qaysi tilda yozsa, shu tilda javob ber (asosan o'zbek, lotin yozuvida). Javob qisqa, aniq va foydali bo'lsin.
QOIDALAR:
1) Faqat o'zing aniq ishonadigan sahih hadis va Qur'on oyatlarini keltir, manbasini ayt (surasi/oyati yoki hadis kitobi).
   Ishonching komil bo'lmasa, hadis TO'QIMA — «aniq bilmayman, ishonchli ulamodan so'rang» de.
2) Fatvo, nikoh-taloq, meros kabi murakkab fiqhiy masalalarda umumiy ma'lumot ber va ishonchli ulamo yoki muftiyatga murojaat qilishni tavsiya qil.
3) Agar foydalanuvchi ma'nosiz, bema'ni, masxara, behuda gap yoki haqorat yozsa — jahl bilan emas, lekin qat'iy: qisqa qilib Jahannam azobini eslat va tavbaga chaqir.
   Masalan: Rasululloh ﷺ: «Kim Allohga va oxirat kuniga iymon keltirgan bo'lsa, yaxshi gapirsin yoki sukut qilsin.» (Buxoriy, Muslim) va Qur'on (Tahrim, 6): «Ey iymon keltirganlar! O'zlaringizni va oilangizni yoqilg'isi odamlar va toshlar bo'lgan do'zaxdan saqlangiz.»
   Oxirida foydali savol berishga yoki Alloh zikriga taklif qil.
4) Oddiy salomga alik ol. Islomga zid, harom yoki zararli ishlarga yo'l ko'rsatma.
5) Siyosiy tortishuvlarga kirma."""

HISTORY = {}
AI_SEM = asyncio.Semaphore(AI_CONCURRENCY)
_rr = itertools.count()


async def ask_ai(uid, name, text):
    if not AI_KEYS:
        return "Suniy intellekt hali ulanmagan (AI_KEYS kiritilmagan)."
    hist = HISTORY.setdefault(uid, [])
    hist.append({"role": "user", "content": text})
    del hist[:-8]
    while hist and hist[0]["role"] != "user":
        hist.pop(0)
    payload = {"model": AI_MODEL, "max_tokens": 800,
               "system": SYSTEM + f"\nFoydalanuvchi ismi: {name}.", "messages": list(hist)}
    async with AI_SEM:
        for attempt in range(len(AI_KEYS) * 2 + 3):
            key = AI_KEYS[next(_rr) % len(AI_KEYS)]
            try:
                async with session.post("https://api.anthropic.com/v1/messages", json=payload,
                                        headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                                 "content-type": "application/json"},
                                        timeout=aiohttp.ClientTimeout(total=60)) as r:
                    data = await r.json()
                    if r.status == 200:
                        out = "".join(b.get("text", "") for b in data.get("content", [])
                                      if b.get("type") == "text").strip()
                        if out:
                            hist.append({"role": "assistant", "content": out})
                            return out
                    elif r.status in (429, 500, 502, 503, 529):
                        await asyncio.sleep(min(1 + attempt, 5))
                    else:
                        log.error("AI xato %s: %s", r.status, data)
            except Exception as e:
                log.warning("AI ulanish xatosi: %s", e)
                await asyncio.sleep(1)
    hist.pop()
    return "Kechirasiz, hozir javob bera olmadim. Birozdan so'ng qayta yozing."


async def answer_long(m: Message, text: str):
    for i in range(0, len(text), 4000):
        await m.answer(text[i:i + 4000], parse_mode=None)


# ====================== HANDLERLAR ======================
@dp.message(CommandStart())
async def h_start(m: Message):
    uid = m.from_user.id
    name = m.from_user.first_name or "aziz do'st"
    upsert_user(uid, name)
    if await is_sub(uid, fresh=True):
        set_sub(uid, 1)
        await m.answer(welcome_text(name))
    else:
        set_sub(uid, 0)
        await m.answer(ask_sub_text(name))


@dp.message(Command("shahar"))
async def h_city(m: Message, command: CommandObject):
    if not await gate(m):
        return
    arg = (command.args or "").strip()
    if not arg:
        await m.answer("Shahar nomini yozing. Masalan: <code>/shahar Samarqand</code> yoki shunchaki «Samarqand» deb yozing. "
                       "Yoki lokatsiyangizni yuboring.")
        return
    c = CITIES.get(norm(arg))
    if c:
        await apply_location(m, c[0], c[1], c[2], "Asia/Tashkent")
        return
    g = await geocode(arg)
    if not g:
        await m.answer("Bu shaharni topa olmadim. Lotin harflarida yozing yoki lokatsiyangizni yuboring.")
        return
    await apply_location(m, g[0], g[1], g[2], g[3])


@dp.message(F.location)
async def h_loc(m: Message):
    if not await gate(m):
        return
    await apply_location(m, "Lokatsiyangiz", m.location.latitude, m.location.longitude)


@dp.message(F.text & ~F.text.startswith("/"))
async def h_text(m: Message):
    if not await gate(m):
        return
    c = CITIES.get(norm(m.text))
    if c:
        await apply_location(m, c[0], c[1], c[2], "Asia/Tashkent")
        return
    await bot.send_chat_action(m.chat.id, ChatAction.TYPING)
    ans = await ask_ai(m.from_user.id, m.from_user.first_name or "do'st", m.text[:2000])
    await answer_long(m, ans)


# ====================== ESLATMALAR (avtomatik) ======================
send_sem = asyncio.Semaphore(25)


async def safe_send(uid, text):
    async with send_sem:
        try:
            await bot.send_message(uid, text)
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after + 1)
            try:
                await bot.send_message(uid, text)
            except Exception:
                pass
        except TelegramForbiddenError:
            db.execute("UPDATE users SET blocked=1 WHERE id=?", (uid,))
            db.commit()
        except Exception as e:
            log.warning("Yuborishda xato %s: %s", uid, e)
        await asyncio.sleep(1)


_cleaned = {"day": ""}


async def tick():
    utc_day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if _cleaned["day"] != utc_day:
        old = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
        db.execute("DELETE FROM sent WHERE key < ?", (old,))
        db.commit()
        _cleaned["day"] = utc_day

    rows = db.execute("SELECT id,name,city,lat,lon,tz FROM users WHERE subscribed=1 AND blocked=0").fetchall()
    jobs = []
    for u in rows:
        try:
            tz = ZoneInfo(u["tz"])
        except Exception:
            tz = ZoneInfo("Asia/Tashkent")
        now = datetime.now(tz)
        today = now.strftime("%Y-%m-%d")
        cur = now.hour * 60 + now.minute
        name = u["name"] or "do'st"
        due = []

        fixed = [("zikr_morning", MORNING_ZIKR_TIME, 60, morning_text(name)),
                 ("zikr_evening", EVENING_ZIKR_TIME, 60, evening_text(name))]
        for i, tm in enumerate(DEATH_TIMES):
            fixed.append((f"death{i}", tm, 60, None))
        for key, (hh, mm), win, txt in fixed:
            start = hh * 60 + mm
            if start <= cur < start + win:
                due.append((key, txt if txt else death_text(name)))

        t = await get_timings(u["lat"], u["lon"], now.strftime("%d-%m-%Y"))
        if t:
            for api, uz in PRAYERS:
                h, mi = map(int, t[api].split(":"))
                start = h * 60 + mi
                if start <= cur < start + 15:
                    due.append((f"pr_{uz}", prayer_text(name, uz, u["city"], t[api])))

        for key, txt in due:
            k = f"{today}:{key}"
            if not was_sent(u["id"], k):
                mark_sent(u["id"], k)
                jobs.append((u["id"], txt))

    if jobs:
        log.info("Eslatmalar yuborilmoqda: %d ta", len(jobs))
        await asyncio.gather(*(safe_send(uid, txt) for uid, txt in jobs))


async def scheduler():
    while True:
        try:
            await tick()
        except Exception as e:
            log.exception("Scheduler xato: %s", e)
        await asyncio.sleep(30)


# ====================== SAYT UCHUN API (obuna + reyting) ======================
def parse_init(init_data: str):
    try:
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
        h = pairs.pop("hash", None)
        check = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
        secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calc = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
        if not h or not hmac.compare_digest(calc, h):
            return None
        if time.time() - int(pairs.get("auth_date", "0")) > 86400:
            return None
        return json.loads(pairs["user"])
    except Exception:
        return None


async def auth_sub(request, fresh=False):
    try:
        body = await request.json()
    except Exception:
        return None, None
    u = parse_init(body.get("initData", ""))
    if not u or not await is_sub(u["id"], fresh=fresh):
        return None, body
    return u, body


@web.middleware
async def cors(request, handler):
    resp = web.Response() if request.method == "OPTIONS" else await handler(request)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return resp


async def api_check(request):
    u, _ = await auth_sub(request, fresh=True)
    if not u:
        return web.json_response({"ok": False}, status=200)
    return web.json_response({"ok": True})


async def api_sync(request):
    u, body = await auth_sub(request)
    if not u:
        return web.json_response({"ok": False}, status=403)
    uid = u["id"]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        want = max(0, int(body.get("score", 0)))
        tas = max(0, int(body.get("tasbeh", 0)))
    except Exception:
        return web.json_response({"ok": False}, status=400)
    row = db.execute("SELECT * FROM scores WHERE uid=?", (uid,)).fetchone()
    old = row["score"] if row else 0
    gain = row["gain"] if row and row["day"] == today else 0
    new = old
    if want > old:
        add = min(want - old, max(0, DAILY_CAP - gain))
        new, gain = old + add, gain + add
    tas = min(tas, (row["tasbeh"] if row else 0) + 3000)
    db.execute("""INSERT INTO scores(uid,name,uname,photo,score,tasbeh,last,day,gain) VALUES(?,?,?,?,?,?,?,?,?)
        ON CONFLICT(uid) DO UPDATE SET name=excluded.name, uname=excluded.uname, photo=excluded.photo,
        score=excluded.score, tasbeh=excluded.tasbeh, last=excluded.last, day=excluded.day, gain=excluded.gain""",
               (uid, u.get("first_name", ""), u.get("username", ""), u.get("photo_url", ""),
                new, tas, int(time.time()), today, gain))
    db.commit()
    return web.json_response({"ok": True, "score": new})


async def api_top(request):
    u, _ = await auth_sub(request)
    if not u:
        return web.json_response({"ok": False}, status=403)
    now, out = int(time.time()), []
    for r in db.execute("SELECT * FROM scores").fetchall():
        ago = max(0, (now - r["last"]) // 86400)
        out.append({"n": r["name"], "u": r["uname"], "ph": r["photo"],
                    "s": max(0, r["score"] - 2 * ago), "ago": ago})  # faol bo'lmasa kuniga -2 ball
    out.sort(key=lambda x: -x["s"])
    return web.json_response({"ok": True, "list": out[:50], "total": len(out),
                              "active": sum(1 for x in out if x["ago"] == 0)})


async def api_health(request):
    return web.Response(text="ok")


# ====================== ISHGA TUSHIRISH ======================
async def main():
    global bot, session
    session = aiohttp.ClientSession()
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))

    await bot.set_my_commands([BotCommand(command="start", description="Boshlash"),
                               BotCommand(command="shahar", description="Shahar tanlash (namoz vaqti uchun)")])
    await bot.set_chat_menu_button(menu_button=MenuButtonWebApp(text="Menyu", web_app=WebAppInfo(url=MINI_APP_URL)))

    app = web.Application(middlewares=[cors])
    app.router.add_post("/api/check", api_check)
    app.router.add_post("/api/sync", api_sync)
    app.router.add_post("/api/top", api_top)
    app.router.add_get("/", api_health)
    runner = web.AppRunner(app)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()

    asyncio.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=False)
    log.info("Bot ishga tushdi")
    try:
        await dp.start_polling(bot)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
