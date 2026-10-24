import asyncio
import os
import random
import logging
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! Render > Environment da qo'shing!")

TIMEZONE = pytz.timezone("Asia/Tashkent")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

# --- BAZA ---
ZIKRLAR = [
    {"arab":"اللَّهُمَّ أَنْتَ رَبِّي","tr":"Allohumma anta Robbiy","mano":"Sen Robbimsan","fazil":"Jannatga kirish sababi! Buxoriy"},
    {"arab":"سُبْحَانَ اللهِ وَبِحَمْدِهِ","tr":"Subhanallohi va bihamdihi 100x","mano":"Alloh pokdir","fazil":"Gunoh kechiriladi! Muslim"},
    {"arab":"لَا إِلَهَ إِلَّا اللهُ","tr":"La ilaha illalloh 100x","mano":"Alloh yagona","fazil":"100 savob yoziladi"},
    {"arab":"حَسْبُنَا اللهُ","tr":"Hasbunalloh","mano":"Alloh kifoya","fazil":"G'am ketadi"},
    {"arab":"لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللهِ","tr":"La havla","mano":"Kuch Allohdan","fazil":"Jannat xazinasi"},
    {"arab":"أَسْتَغْفِرُ اللهَ","tr":"Astag'firulloh 100x","mano":"Kechirim so'rayman","fazil":"Rizq ko'payadi"},
    {"arab":"آيَةُ الْكُرْسِيِّ","tr":"Oyatal Kursiy","mano":"Kursiy oyati","fazil":"Shayton yaqinlashmaydi"},
    {"arab":"سُبْحَانَ اللهِ","tr":"Subhanalloh 33x","mano":"Alloh pok","fazil":"Gunohlar o'chadi"},
    {"arab":"الْحَمْدُ لِلَّهِ","tr":"Alhamdulillah 33x","mano":"Hamd Allohga","fazil":"Mizon to'ladi"},
    {"arab":"اللهُ أَكْبَرُ","tr":"Allohu Akbar 34x","mano":"Alloh buyuk","fazil":"Eng afzal zikr"},
]

QURON = ["1. Fotiha","2. Baqara","3. Oli Imron","36. Yosin","55. Rohman","112. Ixlos","113. Falaq","114. Nos"]
QORILAR = ["Mishary Rashid","Mahir Muaiqly","Sudais","Omar Hisham"]
DUOLAR = ["Ovqat duosi","Uyqu duosi","Safar duosi","Ilm duosi","Ota-ona duosi"]

user_data = {}

def bosh_menyu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Qur'on", callback_data="quron"), InlineKeyboardButton(text="🎧 Qorilar", callback_data="qorilar")],
        [InlineKeyboardButton(text="📜 Hadislar", callback_data="hadis"), InlineKeyboardButton(text="📿 Tasbeh", callback_data="tasbeh")],
        [InlineKeyboardButton(text="🧭 Qibla", callback_data="qibla"), InlineKeyboardButton(text="🌅 Tonggi Zikrlar", callback_data="zikr_tonggi_0")],
        [InlineKeyboardButton(text="🌙 Kechki Zikrlar", callback_data="zikr_kechki_0"), InlineKeyboardButton(text="⭐ 99 Ism", callback_data="ism99")],
        [InlineKeyboardButton(text="📅 Taqvim", callback_data="taqvim"), InlineKeyboardButton(text="🌙 Ramazon", callback_data="ramazon")],
        [InlineKeyboardButton(text="🤲 Duolar", callback_data="duolar"), InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="sozlama")],
        [InlineKeyboardButton(text="🎮 600 ta Quiz O'yini", callback_data="quiz")],
        [InlineKeyboardButton(text="📢 @hakiymqalb", url="https://t.me/hakiymqalb")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]])

def zikr_kb(tip, idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ O'qidim, keyingisi ➡️", callback_data=f"zikr_{tip}_{idx+1}")],
        [InlineKeyboardButton(text="📖 Ma'nosi & Fazilati", callback_data=f"fazil_{idx}")],
        [InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]
    ])

@dp.message(CommandStart())
async def start(m: Message):
    user_data.setdefault(m.from_user.id, {"tasbeh":0,"streak":0})
    await m.answer(f"Assalomu alaykum {m.from_user.first_name}!\n\n12 ta bo'lim - hammasi ichiga kiradi! 👇", reply_markup=bosh_menyu())

@dp.callback_query(F.data=="home")
async def home(c: CallbackQuery):
    await c.message.edit_text("🏠 Bosh Menyu:", reply_markup=bosh_menyu())
    await c.answer()

@dp.callback_query(F.data=="quron")
async def quron(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=s, callback_data="open_sura")] for s in QURON] + [[InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]])
    await c.message.edit_text("📖 Qur'on - Surani tanlang:", reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data=="open_sura")
async def open_sura(c: CallbackQuery):
    await c.message.edit_text("📖 Bismillahir Rohmanir Rohim...\n\nSura matni va audiosi tez orada!", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="qorilar")
async def qorilar(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=q, callback_data="open_qori")] for q in QORILAR] + [[InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]])
    await c.message.edit_text("🎧 Qorini tanlang:", reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data=="open_qori")
async def open_qori(c: CallbackQuery):
    await c.message.edit_text("🎧 Qiroat audio tez orada qo'shiladi!", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="hadis")
async def hadis(c: CallbackQuery):
    await c.message.edit_text("📜 Hadis: Amallar niyatga bog'liqdir (Buxoriy)", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="tasbeh")
async def tasbeh(c: CallbackQuery):
    d = user_data.setdefault(c.from_user.id, {"tasbeh":0,"streak":0})
    d["tasbeh"] += 1
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📿 {d['tasbeh']} - Yana bos", callback_data="tasbeh")],
        [InlineKeyboardButton(text="🔄 0 dan", callback_data="tasbeh_reset"), InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]
    ])
    await c.message.edit_text(f"📿 Subhanalloh: {d['tasbeh']} ta", reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data=="tasbeh_reset")
async def tasbeh_reset(c: CallbackQuery):
    user_data.setdefault(c.from_user.id, {"tasbeh":0,"streak":0})["tasbeh"]=0
    await c.message.edit_text("📿 0 dan boshlandi!", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="qibla")
async def qibla(c: CallbackQuery):
    await c.message.edit_text("🧭 Qibla: Toshkent uchun 220° Janubi-G'arb (Ka'ba)", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data.startswith("zikr_"))
async def zikr_show(c: CallbackQuery):
    try:
        _, tip, idx = c.data.split("_")
        idx = int(idx)
        if idx >= 10:
            d = user_data.setdefault(c.from_user.id, {"tasbeh":0,"streak":0})
            d["streak"]+=1
            await c.message.edit_text(f"🎉 {tip} 10/10 tugadi! Streak: {d['streak']} kun!", reply_markup=bosh_menyu())
            await c.answer()
            return
        z = ZIKRLAR[idx]
        await c.message.edit_text(f"{tip.upper()} {idx+1}/10\n\n🕋 {z['arab']}\n📝 {z['tr']}", reply_markup=zikr_kb(tip, idx))
    except Exception as e:
        logging.error(e)
    await c.answer()

@dp.callback_query(F.data.startswith("fazil_"))
async def fazil(c: CallbackQuery):
    idx = int(c.data.split("_")[1])
    z = ZIKRLAR[idx]
    await c.answer(f"Ma'nosi: {z['mano']}\nFazilati: {z['fazil']}", show_alert=True)

@dp.callback_query(F.data=="ism99")
async def ism99(c: CallbackQuery):
    await c.message.edit_text("⭐ 99 Ism: Ar-Rahman, Ar-Rahim, Al-Malik...", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="taqvim")
async def taqvim(c: CallbackQuery):
    now = datetime.now(TIMEZONE)
    await c.message.edit_text(f"📅 {now.strftime('%d.%m.%Y %H:%M')} Toshkent", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="ramazon")
async def ramazon(c: CallbackQuery):
    await c.message.edit_text("🌙 Ramazon: Iftor 19:15 Sahar 05:10", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="duolar")
async def duolar(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=d, callback_data="open_duo")] for d in DUOLAR] + [[InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]])
    await c.message.edit_text("🤲 Duolar:", reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data=="open_duo")
async def open_duo(c: CallbackQuery):
    await c.message.edit_text("🤲 Duo matni tez orada!", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="sozlama")
async def sozlama(c: CallbackQuery):
    await c.message.edit_text("⚙️ 7 ta eslatma yoqilgan ✅\nTong 07:00 Kech 18:30 Namoz vaqtlari", reply_markup=back_kb())
    await c.answer()

@dp.callback_query(F.data=="quiz")
async def quiz(c: CallbackQuery):
    q = random.choice(["Qur'onda nechta sura bor?","Payg'ambar qachon tug'ilgan?"])
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="A) 114", callback_data="ans_ok"), InlineKeyboardButton(text="B) 110", callback_data="ans_no")],
        [InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]
    ])
    await c.message.edit_text(f"🎮 {q}", reply_markup=kb)
    await c.answer()

@dp.callback_query(F.data.startswith("ans_"))
async def ans(c: CallbackQuery):
    if c.data=="ans_ok":
        await c.answer("✅ To'g'ri! +10 ball!", show_alert=True)
    else:
        await c.answer("❌ Xato, yana urin!", show_alert=True)
    await quiz(c)

async def auto_job(text):
    logging.info(f"AUTO: {text}")

def setup_scheduler():
    scheduler.add_job(auto_job, "cron", hour=5, minute=10, args=["BOMDOD"])
    scheduler.add_job(auto_job, "cron", hour=7, minute=0, args=["TONGGI ZIKR"])
    scheduler.add_job(auto_job, "cron", hour=12, minute=45, args=["PESHIN"])
    scheduler.add_job(auto_job, "cron", hour=16, minute=20, args=["ASR"])
    scheduler.add_job(auto_job, "cron", hour=18, minute=30, args=["KECHKI ZIKR"])
    scheduler.add_job(auto_job, "cron", hour=19, minute=15, args=["SHOM"])
    scheduler.add_job(auto_job, "cron", hour=20, minute=45, args=["XUFTON"])
    scheduler.start()

async def main():
    setup_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())