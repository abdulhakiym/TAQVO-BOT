import asyncio
import json
import logging
import os
import random
import time
from contextlib import suppress
from typing import Any

import aiohttp
from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

# ---------------------------------------------------------------------------
# TAQVO-BOT — Python 3.11+, aiogram 3.x, aiohttp
# Required environment variable: BOT_TOKEN
# Optional: CHANNEL_USERNAME, CHANNEL_URL, SITE_URL, CITY, COUNTRY, PRAYER_METHOD
# Optional reminders: REMINDER_CHAT_IDS is not required; users can enable later.
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("taqvo-bot")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@hakiymqalb")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/hakiymqalb")
SITE_URL = os.getenv("SITE_URL", "https://abdulhakiym.github.io/TAQVO-BOT/")
CITY = os.getenv("CITY", "Tashkent")
COUNTRY = os.getenv("COUNTRY", "Uzbekistan")
PRAYER_METHOD = os.getenv("PRAYER_METHOD", "2")
PORT = int(os.getenv("PORT", "10000"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi. Render Environment Variables ga BOT_TOKEN kiriting.")

# Lightweight in-memory storage. On service restart, scores/settings reset.
# For persistent production data, replace with PostgreSQL/SQLite.
USERS: dict[int, dict[str, Any]] = {}
QUESTION_STATS: dict[int, dict[str, int]] = {}
SESSIONS: aiohttp.ClientSession | None = None
START_TIME = time.time()

# Starter question bank. Add reviewed, sourced questions to reach 600.
SIYRAT_QUESTIONS = [
    {"q": "Payg‘ambarimiz Muhammad ﷺ qayerda tavallud topganlar?", "a": ["Makkada", "Madinada", "Toifda"], "correct": 0, "explain": "U zot ﷺ Makkada tavallud topganlar."},
    {"q": "Payg‘ambarimiz ﷺ ning otalarining ismi nima edi?", "a": ["Abu Tolib", "Abdulloh", "Abdulmuttalib"], "correct": 1, "explain": "Otalarining ismi Abdulloh ibn Abdulmuttalib edi."},
    {"q": "Payg‘ambarimiz ﷺ ning onalarining ismi nima edi?", "a": ["Omina binti Vahb", "Xadicha binti Xuvaylid", "Halima Sa’diya"], "correct": 0, "explain": "Onalarining ismi Omina binti Vahb edi."},
    {"q": "Birinchi vahiy qaysi g‘orda nozil bo‘lgan?", "a": ["Savr", "Hiro", "Uhud"], "correct": 1, "explain": "Birinchi vahiy Hiro g‘orida nozil bo‘lgan."},
    {"q": "Birinchi vahiyda kelgan oyatlar qaysi suradan?", "a": ["Fotiha", "Alaq", "Muddassir"], "correct": 1, "explain": "Alaq surasining dastlabki oyatlari nozil bo‘lgan."},
    {"q": "Payg‘ambarimiz ﷺ ga birinchi vahiy keltirgan farishta kim?", "a": ["Mikoil عليه السلام", "Jabroil عليه السلام", "Isrofil عليه السلام"], "correct": 1, "explain": "Vahiyni Jabroil عليه السلام keltirgan."},
    {"q": "Hijrat qaysi shahardan qaysi shaharga bo‘lgan?", "a": ["Makkadan Madinaga", "Madinadan Shomga", "Toifdan Makkaga"], "correct": 0, "explain": "Musulmonlar Makkadan Madinaga hijrat qilganlar."},
    {"q": "Payg‘ambarimiz ﷺ ning birinchi ayollari kim edilar?", "a": ["Oisha رضي الله عنها", "Xadicha رضي الله عنها", "Hafsa رضي الله عنها"], "correct": 1, "explain": "Birinchi turmush o‘rtoqlari Xadicha رضي الله عنها edilar."},
    {"q": "Payg‘ambarimiz ﷺ qaysi qabiladan edilar?", "a": ["Quraysh", "Aws", "Xazraj"], "correct": 0, "explain": "U zot ﷺ Quraysh qabilasidan edilar."},
    {"q": "Badr jangi hijratning qaysi yilida bo‘lgan?", "a": ["1-yil", "2-yil", "5-yil"], "correct": 1, "explain": "Badr jangi hijratning ikkinchi yilida bo‘lgan."},
    {"q": "Uhud jangi qaysi shaharga yaqin bo‘lgan?", "a": ["Makka", "Madinaga", "Quddus"], "correct": 1, "explain": "Uhud jangi Madina yaqinida bo‘lgan."},
    {"q": "Payg‘ambarimiz ﷺ ning bobolari kim edi?", "a": ["Abdulmuttalib", "Abu Sufyon", "Abu Lahab"], "correct": 0, "explain": "Bobolarining ismi Abdulmuttalib edi."},
    {"q": "Payg‘ambarimiz ﷺ ning emizgan onalaridan mashhuri kim?", "a": ["Halima Sa’diya", "Safiyya", "Maymuna"], "correct": 0, "explain": "Halima Sa’diya رضي الله عنها u zotni emizganlar."},
    {"q": "Qur’on qaysi tilda nozil qilingan?", "a": ["Forscha", "Arabcha", "Ibroniycha"], "correct": 1, "explain": "Qur’oni Karim arab tilida nozil qilingan."},
    {"q": "Payg‘ambarimiz ﷺ Madinaga kelganlarida qaysi masjidni qurishda qatnashganlar?", "a": ["Qubo masjidi", "Aqso masjidi", "Azhar masjidi"], "correct": 0, "explain": "Qubo masjidining qurilishida qatnashganlar."},
    {"q": "Payg‘ambarimiz ﷺ ning kunyalaridan biri qaysi?", "a": ["Abul Qosim", "Abu Hurayra", "Abu Bakr"], "correct": 0, "explain": "U zot ﷺ ning kunyalaridan biri Abul Qosim."},
    {"q": "Makkadan Madinaga hijratda Payg‘ambarimiz ﷺ ga hamroh bo‘lgan sahoba kim?", "a": ["Umar ibn Xattob رضي الله عنه", "Abu Bakr Siddiq رضي الله عنه", "Usmon ibn Affon رضي الله عنه"], "correct": 1, "explain": "Hijrat safarida Abu Bakr رضي الله عنه hamroh bo‘lganlar."},
    {"q": "Payg‘ambarimiz ﷺ ning qizlaridan biri kim?", "a": ["Fotima رضي الله عنها", "Maryam عليها السلام", "Osiyo رضي الله عنها"], "correct": 0, "explain": "Fotima رضي الله عنها u zotning qizlaridan edilar."},
    {"q": "Ka’bani qayta qurishda Quraysh bilan birga qatnashganlarida Payg‘ambarimiz ﷺ taxminan necha yoshda edilar?", "a": ["35 yosh", "25 yosh", "40 yosh"], "correct": 0, "explain": "Mashhur siyrat rivoyatlarida 35 yosh deb keltiriladi."},
    {"q": "Payg‘ambarimiz ﷺ qayerda vafot etganlar?", "a": ["Makkada", "Madinada", "Toifda"], "correct": 1, "explain": "U zot ﷺ Madinai Munavvarada vafot etganlar."},
]

def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📖 Siyrat savollari"), KeyboardButton(text="📿 Tasbeh")],
            [KeyboardButton(text="🌅 Tonggi zikr"), KeyboardButton(text="🌙 Kechki zikr")],
            [KeyboardButton(text="🕌 Namoz vaqtlari"), KeyboardButton(text="🏆 Reyting")],
            [KeyboardButton(text="🤖 TAQVO AI"), KeyboardButton(text="🌐 TAQVO SAYT", web_app=None)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo‘limni tanlang",
    )

def subscription_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check")],
    ])

def user_record(user_id: int) -> dict[str, Any]:
    if user_id not in USERS:
        USERS[user_id] = {"score": 0, "tasbeh": 0, "last_question": None, "awaiting_ai": False}
    return USERS[user_id]

async def is_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status not in ("left", "kicked", "restricted")
    except (TelegramBadRequest, TelegramForbiddenError) as exc:
        log.warning("Obuna tekshiruvi xatosi: %s", exc)
        return False
    except Exception:
        log.exception("Obunani tekshirishda noma'lum xato")
        return False

async def require_subscription(message: Message, bot: Bot) -> bool:
    if message.from_user and await is_subscribed(bot, message.from_user.id):
        return True
    await message.answer(
        "TAQVO-BOT’dan foydalanish uchun avval @hakiymqalb kanaliga obuna bo‘ling.",
        reply_markup=subscription_keyboard(),
    )
    return False

async def get_prayer_times(session: aiohttp.ClientSession) -> str:
    url = "https://api.aladhan.com/v1/timingsByCity"
    params = {"city": CITY, "country": COUNTRY, "method": PRAYER_METHOD}
    try:
        async with session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=15)) as response:
            response.raise_for_status()
            data = await response.json()
        timings = data.get("data", {}).get("timings", {})
        date = data.get("data", {}).get("date", {}).get("readable", "")
        keys = [("Bomdod", "Fajr"), ("Quyosh", "Sunrise"), ("Peshin", "Dhuhr"),
                ("Asr", "Asr"), ("Shom", "Maghrib"), ("Xufton", "Isha")]
        lines = [f"🕌 <b>Namoz vaqtlari — {CITY}</b>", f"📅 {date}", ""]
        for uz, key in keys:
            if timings.get(key):
                lines.append(f"• {uz}: <b>{timings[key]}</b>")
        lines += ["", "Vaqtlar API ma’lumotiga asoslangan. Mahalliy masjid taqvimi bilan solishtiring."]
        return "\n".join(lines)
    except Exception as exc:
        log.warning("Namoz vaqti API xatosi: %s", exc)
        return "Namoz vaqtlarini hozir olib bo‘lmadi. Internet/API holatini tekshirib, qayta urinib ko‘ring."

def question_keyboard(question: dict[str, Any], qid: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=answer, callback_data=f"answer:{qid}:{i}")]
        for i, answer in enumerate(question["a"])
    ])

async def send_random_question(message: Message) -> None:
    qid = random.randrange(len(SIYRAT_QUESTIONS))
    question = SIYRAT_QUESTIONS[qid]
    user_record(message.from_user.id)
    USERS[message.from_user.id]["last_question"] = qid
    await message.answer(
        f"📖 <b>Siyrat savoli</b>\n\n{question['q']}",
        reply_markup=question_keyboard(question, qid),
    )

async def scheduler(bot: Bot) -> None:
    # Scheduler loop is intentionally conservative. User reminders need opt-in and
    # timezone persistence; this starter avoids unsolicited messages.
    while True:
        await asyncio.sleep(3600)

async def api_health(request: web.Request) -> web.Response:
    return web.json_response({
        "ok": True, "service": "TAQVO-BOT", "uptime_seconds": int(time.time() - START_TIME)
    })

async def api_check(request: web.Request) -> web.Response:
    user_id = request.query.get("user_id")
    if not user_id:
        try:
            body = await request.json()
            user_id = str(body.get("user_id", ""))
        except Exception:
            user_id = ""
    if not user_id.isdigit():
        return web.json_response({"ok": False, "error": "user_id integer bo‘lishi kerak"}, status=400)
    record = user_record(int(user_id))
    return web.json_response({"ok": True, "user_id": int(user_id), "score": record["score"]})

async def api_sync(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.json_response({"ok": False, "error": "JSON kerak"}, status=400)
    user_id = body.get("user_id")
    if not isinstance(user_id, int) or user_id <= 0:
        return web.json_response({"ok": False, "error": "user_id musbat integer bo‘lishi kerak"}, status=400)
    record = user_record(user_id)
    # Only accept a non-negative score; do not allow arbitrary score reduction.
    score = body.get("score")
    if isinstance(score, int) and score >= record["score"]:
        record["score"] = min(score, 1_000_000)
    return web.json_response({"ok": True, "user_id": user_id, "score": record["score"]})

async def api_top(request: web.Request) -> web.Response:
    top = sorted(
        ({"user_id": uid, "score": data["score"]} for uid, data in USERS.items()),
        key=lambda item: item["score"], reverse=True
    )[:10]
    return web.json_response({"ok": True, "top": top})

def create_web_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", api_health)
    app.router.add_get("/api/check", api_check)
    app.router.add_post("/api/check", api_check)
    app.router.add_post("/api/sync", api_sync)
    app.router.add_get("/api/top", api_top)
    cors = cors_setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=False,
            expose_headers="*",
            allow_headers="*",
            allow_methods=("GET", "POST", "OPTIONS"),
        )
    })
    # Register CORS on all resources after routes are created.
    for route in list(app.router.routes()):
        with suppress(Exception):
            cors.add(route)
    return app

async def on_start(message: Message, bot: Bot) -> None:
    if not message.from_user:
        return
    user_record(message.from_user.id)
    if not await require_subscription(message, bot):
        return
    await message.answer(
        "Assalomu alaykum! 🌿\n\nTAQVO-BOT’ga xush kelibsiz. Bo‘limni tanlang.",
        reply_markup=main_keyboard(),
    )

async def on_check(callback: CallbackQuery, bot: Bot) -> None:
    if not callback.from_user:
        await callback.answer()
        return
    if await is_subscribed(bot, callback.from_user.id):
        await callback.message.answer("✅ Obuna tasdiqlandi. Endi /start buyrug‘ini bosing.")
    else:
        await callback.answer("Avval kanalga obuna bo‘ling, so‘ng qayta tekshiring.", show_alert=True)

async def on_answer(callback: CallbackQuery) -> None:
    try:
        _, qid_s, answer_s = callback.data.split(":")
        qid, answer_idx = int(qid_s), int(answer_s)
        question = SIYRAT_QUESTIONS[qid]
    except Exception:
        await callback.answer("Savol ma’lumoti topilmadi.", show_alert=True)
        return
    record = user_record(callback.from_user.id)
    if record.get("last_question") != qid:
        await callback.answer("Bu savol eskirgan. Yangi savol oling.", show_alert=True)
        return
    record["last_question"] = None
    if answer_idx == question["correct"]:
        record["score"] += 1
        result = f"✅ To‘g‘ri! +1 ball.\n\n{question['explain']}"
    else:
        result = f"❌ Bu javob to‘g‘ri emas.\nTo‘g‘ri javob: <b>{question['a'][question['correct']]}</b>\n\n{question['explain']}"
    with suppress(Exception):
        await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(f"{result}\n\n🏆 Jami ballingiz: <b>{record['score']}</b>")
    await callback.answer()

async def on_text(message: Message, bot: Bot, session: aiohttp.ClientSession) -> None:
    if not message.from_user or not message.text:
        return
    if not await require_subscription(message, bot):
        return
    record = user_record(message.from_user.id)
    text = message.text.strip()

    if text == "📖 Siyrat savollari":
        await send_random_question(message)
    elif text == "📿 Tasbeh":
        record["tasbeh"] = 0
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📿 +1", callback_data="tasbeh:add"),
             InlineKeyboardButton(text="🔄 Nolga tushirish", callback_data="tasbeh:reset")]
        ])
        await message.answer(
            "📿 <b>Tasbeh</b>\n\nSubhanalloh — 33 marta\nAlhamdulillah — 33 marta\nAllohu Akbar — 34 marta\n\nHisoblagich: <b>0</b>",
            reply_markup=kb,
        )
    elif text == "🌅 Tonggi zikr":
        await message.answer(
            "🌅 <b>Tonggi zikr</b>\n\n"
            "سُبْحَانَ اللهِ وَبِحَمْدِهِ\n"
            "Subhanallohi va bihamdihi.\n"
            "Ma’nosi: Allohni hamd bilan poklab yod etaman.\n"
            "📿 100 marta.\n\n"
            "Manba: Sahih al-Buxoriyda kelgan zikr. Zikrning lafzi va dalilini ishonchli nashrdan tekshiring."
        )
    elif text == "🌙 Kechki zikr":
        await message.answer(
            "🌙 <b>Kechki zikr</b>\n\n"
            "Oyatul Kursiy — Baqara surasi, 255-oyat.\n"
            "Arabcha tilovatni Qur’on mushafidan o‘qing. Ma’nosini ham o‘rganing.\n\n"
            "Eslatma: tonggi-kechki zikrlar ro‘yxati kengaytirilishi va har bir rivoyat alohida tekshirilishi kerak."
        )
    elif text == "🕌 Namoz vaqtlari":
        await message.answer(await get_prayer_times(session), parse_mode=ParseMode.HTML)
    elif text == "🏆 Reyting":
        top = sorted(USERS.items(), key=lambda item: item[1]["score"], reverse=True)[:10]
        lines = ["🏆 <b>TAQVO-BOT reytingi</b>", f"Sizning ballingiz: <b>{record['score']}</b>", ""]
        if not top or all(v["score"] == 0 for _, v in top):
            lines.append("Siyrat savollariga javob berib ball to‘plang!")
        else:
            for index, (uid, data) in enumerate(top, 1):
                lines.append(f"{index}. Foydalanuvchi {uid}: {data['score']} ball")
        await message.answer("\n".join(lines), parse_mode=ParseMode.HTML)
    elif text == "🤖 TAQVO AI":
        record["awaiting_ai"] = True
        await message.answer(
            "🤖 <b>TAQVO AI</b>\n\nIslomiy savolingizni yozing. Hozirgi versiya savolni qabul qiladi, "
            "lekin haqiqiy AI javobi uchun AI API xizmati ulanmagan.\n\n"
            "Qur’on va sahih Sunnat asosida tekshirilgan javob izlang. Aniq fatvo uchun malakali olimga murojaat qiling."
        )
    elif text == "🌐 TAQVO SAYT":
        await message.answer(f"🌐 TAQVO SAYT:\n{SITE_URL}")
    elif record.get("awaiting_ai"):
        record["awaiting_ai"] = False
        # No fake AI answer: acknowledge receipt and provide a safe limitation.
        await message.answer(
            "Savolingiz qabul qilindi. Bu versiyada AI modeli ulanmaganligi sababli avtomatik fatvo bermayman.\n\n"
            "Savolni Qur’on, sahih hadis manbalari va ishonchli olimlar izohi bilan tekshiring. "
            "Shaxsiy fatvo uchun malakali olimga murojaat qiling."
        )
    else:
        await message.answer("Iltimos, menyudagi bo‘limlardan birini tanlang.", reply_markup=main_keyboard())

async def on_tasbeh(callback: CallbackQuery) -> None:
    record = user_record(callback.from_user.id)
    if callback.data == "tasbeh:reset":
        record["tasbeh"] = 0
    else:
        record["tasbeh"] += 1
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📿 +1", callback_data="tasbeh:add"),
         InlineKeyboardButton(text="🔄 Nolga tushirish", callback_data="tasbeh:reset")]
    ])
    with suppress(Exception):
        await callback.message.edit_text(
            f"📿 <b>Tasbeh</b>\n\nHisoblagich: <b>{record['tasbeh']}</b>",
            reply_markup=kb,
        )
    await callback.answer(str(record["tasbeh"]))

async def main() -> None:
    global SESSIONS
    session = aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=20),
        headers={"User-Agent": "TAQVO-BOT/1.0"},
    )
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    app = create_web_app()
    runner = web.AppRunner(app)
    scheduler_task: asyncio.Task | None = None

    dp.message.register(on_start, CommandStart())
    dp.callback_query.register(on_check, F.data == "check")
    dp.callback_query.register(on_answer, F.data.startswith("answer:"))
    dp.callback_query.register(on_tasbeh, F.data.startswith("tasbeh:"))
    dp.message.register(on_text, F.text)

    # Middleware-like dependency injection for the shared aiohttp session.
    # aiogram handler kwargs are populated through workflow data.
    dp["session"] = session
    dp["bot"] = bot

    # The message handler receives session through dispatcher workflow data.
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await runner.setup()
        site = web.TCPSite(runner, host="0.0.0.0", port=PORT)
        await site.start()
        scheduler_task = asyncio.create_task(scheduler(bot), name="taqvo-scheduler")
        log.info("Bot ishga tushdi; HTTP port=%s", PORT)
        await dp.start_polling(bot, session=session)
    finally:
        if scheduler_task:
            scheduler_task.cancel()
            with suppress(asyncio.CancelledError):
                await scheduler_task
        await bot.session.close()
        await session.close()
        await runner.cleanup()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("TAQVO-BOT to‘xtatildi")
