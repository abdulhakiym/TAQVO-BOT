import asyncio
import os
import random
import logging
import pytz
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, MenuButtonWebApp, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

TIMEZONE = pytz.timezone("Asia/Tashkent")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

# --- BAZA ---
ZIKRLAR = [
    {"arab":"اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ","tr":"Allohumma anta Robbiy","mano":"Sen Robbimsan","fazil":"💎 Jannatga kirish sababi! Buxoriy 6306"},
    {"arab":"سُبْحَانَ اللهِ وَبِحَمْدِهِ 100x","tr":"Subhanallohi va bihamdihi","mano":"Alloh pokdir","fazil":"💎 Gunoh dengiz ko'pigi bo'lsa ham kechiriladi! Muslim 2691"},
    {"arab":"لَا إِلَهَ إِلَّا اللهُ","tr":"La ilaha illalloh","mano":"Allohdan o'zga iloh yo'q","fazil":"💎 100 savob, shaytondan himoya!"},
    {"arab":"حَسْبُنَا اللهُ وَنِعْمَ الْوَكِيلُ","tr":"Hasbunalloh","mano":"Alloh kifoya","fazil":"💎 G'am ketadi!"},
    {"arab":"لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللهِ","tr":"La havla","mano":"Kuch Allohdan","fazil":"💎 Jannat xazinasi!"},
    {"arab":"أَسْتَغْفِرُ اللهَ 100x","tr":"Astag'firulloh","mano":"Kechirim so'rayman","fazil":"💎 Rizq ko'payadi!"},
    {"arab":"آيَةُ الْكُرْسِيِّ","tr":"Oyatal Kursiy","mano":"Kursiy oyati","fazil":"💎 Shayton yaqinlashmaydi!"},
    {"arab":"سُبْحَانَ اللهِ 33x","tr":"Subhanalloh 33","mano":"Alloh pok","fazil":"💎 Gunohlar kechiriladi!"},
    {"arab":"الْحَمْدُ لِلَّهِ 33x","tr":"Alhamdulillah 33","mano":"Hamd Allohga","fazil":"💎 Tarozini to'ldiradi!"},
    {"arab":"اللهُ أَكْبَرُ 34x","tr":"Allohu Akbar 34","mano":"Alloh buyuk","fazil":"💎 Eng afzal zikr!"},
]

SAVOLLAR = [
    {"id":i, "cat":"40 Farz" if i<=40 else "Siyrat" if i<=300 else "Islom", 
     "q":f"{i}-savol: Payg'ambarimiz qachon tug'ilganlar?" if i==1 else f"Savol {i} - {('40 Farz' if i<=40 else 'Siyrat' if i<=300 else 'Islom')}",
     "a":["570-yil","571-yil","632-yil"], "t":"571-yil", "f":"Fazilat: Ilm o'rganish farz!"}
    for i in range(1,601)
]

QURON = ["1. Fotiha","2. Baqara","3. Oli Imron"]
user_data = {}

# --- BURCHAKDAN SAYT OCHISH ---
async def setup_menu_button():
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🕌 TAQVO SAYT",
                web_app=WebAppInfo(url="https://abdulhakiym.github.io/TAQVO-BOT/")
            )
        )
        print("✅ Burchak tugmasi o'rnatildi!")
    except Exception as e:
        print(f"Menu error: {e}")

# --- MENYULAR - HAMMASI JAMLANGAN ---
def asosiy_menyu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌅 Tonggi Zikr (1/10) 🔥", callback_data="zikr_tonggi_0"), 
         InlineKeyboardButton(text="🌙 Kechki Zikr (1/10) 🌙", callback_data="zikr_kechki_0")],
        [InlineKeyboardButton(text="🎮 Siyrat O'yini (600 savol)", callback_data="game_start")],
        [InlineKeyboardButton(text="📚 40 Farz Testi", callback_data="farz_start"), 
         InlineKeyboardButton(text="📖 Islom 300 Testi", callback_data="islom_start")],
        [InlineKeyboardButton(text="🕋 Namoz Vaqtlari", callback_data="namoz"),
         InlineKeyboardButton(text="📿 Tasbeh (33/99)", callback_data="tasbeh")],
        [InlineKeyboardButton(text="🏆 Reyting & Streak 🔥", callback_data="top"), 
         InlineKeyboardButton(text="📖 Fazilatlar", callback_data="fazilatlar")],
        [InlineKeyboardButton(text="🕌 Saytni Ochish (burchakdan ham)", web_app=WebAppInfo(url="https://abdulhakiym.github.io/TAQVO-BOT/"))],
        [InlineKeyboardButton(text="📢 @hakiymqalb Kanal", url="https://t.me/hakiymqalb")]
    ])

def zikr_kb(tip, idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ O'qidim, keyingisi ➡️", callback_data=f"zikr_{tip}_{idx+1}")],
        [InlineKeyboardButton(text="📖 Ma'nosi & Fazilati 💎", callback_data=f"fazil_{idx}")],
        [InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]
    ])

@dp.message(CommandStart())
async def start(m: Message):
    user_data.setdefault(m.from_user.id, {"ball":0,"streak":0,"tasbeh":0,"used":set()})
    await m.answer(
        f"🤲 Assalomu alaykum {m.from_user.first_name}!\n\n"
        "🔥 TAQVO PRO - FINAL 🔥\n\n"
        "✅ 600 ta o'yin savoli\n✅ Burchakdan sayt ochiladi\n✅ 10 ta zikr ketma-ket\n✅ Streak, Reyting, Tasbeh\n\n"
        "👇 Menyu tanlang - pastki chap burchakdan ham sayt ochiladi!",
        reply_markup=asosiy_menyu()
    )

@dp.callback_query(F.data.startswith("zikr_"))
async def zikr_show(c: CallbackQuery):
    _, tip, idx = c.data.split("_"); idx=int(idx)
    if idx>=10:
        user_data[c.from_user.id]["streak"]+=1
        await c.message.answer(f"🎉 {tip.upper()} 10/10 TUGADI!\n🔥 Streak: {user_data[c.from_user.id]['streak']} kun!", reply_markup=asosiy_menyu())
        return
    z=ZIKRLAR[idx]
    await c.message.answer(f"**{tip.upper()} ZIKR {idx+1}/10**\n\n🕋 {z['arab']}\n\n📝 {z['tr']}", reply_markup=zikr_kb(tip, idx), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("fazil_"))
async def fazil_show(c: CallbackQuery):
    idx=int(c.data.split("_")[1]); z=ZIKRLAR[idx]
    await c.answer(f"MA'NOSI: {z['mano']}\n\nFAZILATI:\n{z['fazil']}", show_alert=True)

@dp.callback_query(F.data=="game_start")
async def game(c: CallbackQuery):
    q = random.choice([s for s in SAVOLLAR if s["id"] not in user_data[c.from_user.id]["used"]])
    user_data[c.from_user.id]["used"].add(q["id"])
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=a, callback_data=f"ans_{a}_{q['id']}")] for a in q["a"]
    ] + [[InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]])
    await c.message.answer(f"🎮 {q['cat']} - {q['id']}/600\n\n{q['q']}\n\nBall: {user_data[c.from_user.id]['ball']}", reply_markup=kb)

@dp.callback_query(F.data.startswith("ans_"))
async def ans(c: CallbackQuery):
    _, javob, qid = c.data.split("_"); qid=int(qid)
    q = next(s for s in SAVOLLAR if s["id"]==qid)
    if javob==q["t"]:
        user_data[c.from_user.id]["ball"]+=10
        await c.answer(f"✅ To'g'ri! +10 ball!\nFazilat: {q['f']}", show_alert=True)
    else:
        await c.answer(f"❌ Xato! To'g'ri: {q['t']}\n{q['f']}", show_alert=True)
    await game(c)

@dp.callback_query(F.data=="tasbeh")
async def tasbeh(c: CallbackQuery):
    user_data[c.from_user.id]["tasbeh"]+=1
    cnt=user_data[c.from_user.id]["tasbeh"]
    kb=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📿 {cnt} - BOSING", callback_data="tasbeh")],
        [InlineKeyboardButton(text="🔄 0 dan boshlash", callback_data="tasbeh_reset"), InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]
    ])
    await c.message.answer(f"📿 Subhanalloh: {cnt}/33", reply_markup=kb)

@dp.callback_query(F.data=="home")
async def home(c: CallbackQuery):
    await c.message.answer("🏠 Bosh Menyu:", reply_markup=asosiy_menyu())

def setup_scheduler():
    scheduler.add_job(lambda: print("BOMDOD"), "cron", hour=5, minute=10)
    scheduler.add_job(lambda: print("TONGGI ZIKR"), "cron", hour=7, minute=0)
    scheduler.add_job(lambda: print("KECHKI ZIKR"), "cron", hour=18, minute=30)
    scheduler.start()

async def main():
    setup_scheduler()
    await setup_menu_button()
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())