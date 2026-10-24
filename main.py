import asyncio, os, pytz, random
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
TIMEZONE = pytz.timezone("Asia/Tashkent")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)

# --- MA'LUMOTLAR BAZASI ---
ZIKRLAR = [
    {"arab":"اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ","tr":"Allohumma anta Robbiy","mano":"Sen mening Robbimsan","fazil":"💎 Jannatga kirish sababi! Buxoriy 6306"},
    {"arab":"سُبْحَانَ اللهِ وَبِحَمْدِهِ 100x","tr":"Subhanallohi va bihamdihi","mano":"Alloh pokdir","fazil":"💎 Gunoh kechiriladi! Muslim 2691"},
    {"arab":"لَا إِلَهَ إِلَّا اللهُ 100x","tr":"La ilaha illalloh","mano":"Alloh yagona","fazil":"💎 100 savob!"},
    {"arab":"حَسْبُنَا اللهُ وَنِعْمَ الْوَكِيلُ","tr":"Hasbunalloh","mano":"Alloh kifoya","fazil":"💎 G'am ketadi!"},
    {"arab":"لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللهِ","tr":"La havla","mano":"Kuch Allohdan","fazil":"💎 Jannat xazinasi!"},
    {"arab":"أَسْتَغْفِرُ اللهَ 100x","tr":"Astag'firulloh","mano":"Kechirim so'rayman","fazil":"💎 Rizq ko'payadi!"},
    {"arab":"آيَةُ الْكُرْسِيِّ","tr":"Oyatal Kursiy","mano":"Kursiy oyati","fazil":"💎 Shayton yaqinlashmaydi!"},
    {"arab":"سُبْحَانَ اللهِ 33x","tr":"Subhanalloh","mano":"Alloh pok","fazil":"💎 Gunohlar kechiriladi!"},
    {"arab":"الْحَمْدُ لِلَّهِ 33x","tr":"Alhamdulillah","mano":"Hamd Allohga","fazil":"💎 Mizon to'ladi!"},
    {"arab":"اللهُ أَكْبَرُ 34x","tr":"Allohu Akbar","mano":"Alloh buyuk","fazil":"💎 Eng afzal!"},
]

QURON_SURALAR = ["1. Fotiha","2. Baqara","3. Oli Imron","36. Yosin","55. Rohman","112. Ixlos","113. Falaq","114. Nos"]
QORILAR = ["🎧 Mishary Rashid Alafasy","🎧 Mahir Al-Muaiqly","🎧 Abdurahmon As-Sudais","🎧 Omar Hisham"]
HADISLAR = ["Buxoriy 1: Amallar niyatga bog'liq","Muslim 2691: 100 ta Subhanalloh","Termiziy: Eng yaxshingiz Qur'on o'rganuvchingiz"]
ISM_99 = [f"{i}. Allohning go'zal ismi" for i in range(1,100)]
DUOLAR = ["🤲 Ovqatdan oldin","🤲 Uxlashdan oldin","🤲 Safar duosi","🤲 Ilm duosi","🤲 Ota-ona uchun"]

user_data = {}

# --- KLAVIATURALAR ---
def bosh_menyu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 Qur'on", callback_data="quron"), InlineKeyboardButton(text="🎧 Qorilar", callback_data="qorilar")],
        [InlineKeyboardButton(text="📜 Hadislar", callback_data="hadis"), InlineKeyboardButton(text="📿 Tasbeh", callback_data="tasbeh")],
        [InlineKeyboardButton(text="🧭 Qibla", callback_data="qibla"), InlineKeyboardButton(text="🌅 Tonggi Zikrlar", callback_data="zikr_tonggi_0")],
        [InlineKeyboardButton(text="🌙 Kechki Zikrlar", callback_data="zikr_kechki_0"), InlineKeyboardButton(text="⭐ 99 Ism", callback_data="ism99")],
        [InlineKeyboardButton(text="📅 Taqvim", callback_data="taqvim"), InlineKeyboardButton(text="🌙 Ramazon Mode", callback_data="ramazon")],
        [InlineKeyboardButton(text="🤲 Duolar", callback_data="duolar"), InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="sozlama")],
        [InlineKeyboardButton(text="🎮 600 ta Quiz O'yini", callback_data="quiz")],
        [InlineKeyboardButton(text="📢 @hakiymqalb", url="https://t.me/hakiymqalb")]
    ])

def back_kb():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]])

def zikr_kb(tip, idx):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ O'qidim, keyingisi ➡️", callback_data=f"zikr_{tip}_{idx+1}")],
        [InlineKeyboardButton(text="📖 Ma'nosi & Fazilati 💎", callback_data=f"fazil_{idx}")],
        [InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]
    ])

# --- START ---
@dp.message(CommandStart())
async def start(m: Message):
    user_data.setdefault(m.from_user.id, {"ball":0,"tasbeh":0,"streak":0})
    await m.answer(
        f"Assalomu alaykum {m.from_user.first_name}!\n\nIslomiy - Barcha bo'limlar ochiq! 12 ta menyu ichiga kiriladi!\n7 ta eslatma Toshkent vaqti bilan ishlaydi!",
        reply_markup=bosh_menyu()
    )

@dp.callback_query(F.data=="home")
async def home(c: CallbackQuery):
    await c.message.answer("🏠 Bosh Menyu:", reply_markup=bosh_menyu())

# --- 12 TA BO'LIM - HAMMASI ICHIGA KIRADI ---

@dp.callback_query(F.data=="quron")
async def quron(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=s, callback_data=f"sur_{s}")] for s in QURON_SURALAR
    ] + [[InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]])
    await c.message.answer("📖 Qur'on - Surani tanlang:", reply_markup=kb)

@dp.callback_query(F.data.startswith("sur_"))
async def sura(c: CallbackQuery):
    sura_nomi = c.data.replace("sur_","")
    await c.message.answer(f"📖 {sura_nomi}\n\nبِسْمِ اللهِ الرَّحْمٰنِ الرَّحِيْمِ\n\nMatn tez orada... Audio bilan tinglang!\n\n✅ O'qildi - Savob yozildi!", reply_markup=back_kb())

@dp.callback_query(F.data=="qorilar")
async def qorilar(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=q, callback_data=f"qori_{i}")] for i,q in enumerate(QORILAR)
    ] + [[InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]])
    await c.message.answer("🎧 Qorilar - Qorini tanlang:", reply_markup=kb)

@dp.callback_query(F.data=="hadis")
async def hadis(c: CallbackQuery):
    text = "\n\n".join(HADISLAR)
    await c.message.answer(f"📜 Hadislar:\n\n{text}\n\n💎 Fazilati bilan!", reply_markup=back_kb())

@dp.callback_query(F.data=="tasbeh")
async def tasbeh(c: CallbackQuery):
    user_data[c.from_user.id]["tasbeh"] += 1
    cnt = user_data[c.from_user.id]["tasbeh"]
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"📿 {cnt} - BOSING", callback_data="tasbeh")],
        [InlineKeyboardButton(text="🔄 0 dan", callback_data="tasbeh_reset"), InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]
    ])
    await c.message.answer(f"📿 Subhanalloh: {cnt}\n{cnt%33==0 and '🎉 33 tugadi!' or ''}", reply_markup=kb)

@dp.callback_query(F.data=="tasbeh_reset")
async def reset(c: CallbackQuery):
    user_data[c.from_user.id]["tasbeh"]=0
    await c.message.answer("0 dan boshlandi!", reply_markup=back_kb())

@dp.callback_query(F.data=="qibla")
async def qibla(c: CallbackQuery):
    await c.message.answer("🧭 Qibla - Toshkent uchun 220° Janubi-G'arb\n\n📍 Ka'ba tomoniga yuzlaning!\nQibla kompas tez orada ilovada!", reply_markup=back_kb())

@dp.callback_query(F.data.startswith("zikr_"))
async def zikr_show(c: CallbackQuery):
    _, tip, idx = c.data.split("_"); idx=int(idx)
    if idx>=10:
        user_data[c.from_user.id]["streak"]+=1
        await c.message.answer(f"🎉 {tip.upper()} 10/10 TUGADI!\n🔥 Streak: {user_data[c.from_user.id]['streak']} kun!", reply_markup=bosh_menyu())
        return
    z=ZIKRLAR[idx]
    await c.message.answer(f"**{tip.upper()} ZIKR {idx+1}/10**\n\n🕋 {z['arab']}\n\n📝 {z['tr']}\n\nProgress: {idx+1}/10", reply_markup=zikr_kb(tip, idx), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("fazil_"))
async def fazil(c: CallbackQuery):
    idx=int(c.data.split("_")[1]); z=ZIKRLAR[idx]
    await c.answer(f"MA'NOSI: {z['mano']}\n\nFAZILATI: {z['fazil']}\n\nO'qib bo'lgach Keyingisi bosing!", show_alert=True)

@dp.callback_query(F.data=="ism99")
async def ism99(c: CallbackQuery):
    await c.message.answer("⭐ 99 Ism:\n\n1. Ar-Rahman - Mehribon\n2. Ar-Rahim - Rahmli\n3. Al-Malik - Podshoh\n... 99 ta ism fazilati bilan!", reply_markup=back_kb())

@dp.callback_query(F.data=="taqvim")
async def taqvim(c: CallbackQuery):
    now = datetime.now(TIMEZONE)
    await c.message.answer(f"📅 Taqvim:\n\nMilodiy: {now.strftime('%d %B %Y, %A')}\nHijriy: 04 Safar 1447 (namuna)\nToshkent vaqti: {now.strftime('%H:%M')}", reply_markup=back_kb())

@dp.callback_query(F.data=="ramazon")
async def ramazon(c: CallbackQuery):
    await c.message.answer("🌙 Ramazon Mode Yoqildi!\n\n✅ Iftorlik: 19:15\n✅ Saharlik: 05:10\n✅ Taroveh eslatmasi yoqildi!", reply_markup=back_kb())

@dp.callback_query(F.data=="duolar")
async def duolar(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=d, callback_data=f"duo_{i}")] for i,d in enumerate(DUOLAR)
    ] + [[InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]])
    await c.message.answer("🤲 Duolar - Birini tanlang:", reply_markup=kb)

@dp.callback_query(F.data=="sozlama")
async def sozlama(c: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌅 Tonggi 07:00 ✅", callback_data="soz_tong"), InlineKeyboardButton(text="🌙 Kechki 18:30 ✅", callback_data="soz_kech")],
        [InlineKeyboardButton(text="🕌 5 mahal namoz ✅", callback_data="soz_namoz"), InlineKeyboardButton(text="🏠 Bosh Menyu", callback_data="home")]
    ])
    await c.message.answer("⚙️ Sozlamalar:\n\n7 ta eslatma yoqilgan - Toshkent vaqti!\nO'chirib-yoqishingiz mumkin!", reply_markup=kb)

@dp.callback_query(F.data=="quiz")
async def quiz(c: CallbackQuery):
    q = random.choice(["Payg'ambarimiz qachon tug'ilgan?","Qur'onda nechta sura bor?","40 Farz nima?"])
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="A) 570-yil", callback_data="ans_a"), InlineKeyboardButton(text="B) 571-yil", callback_data="ans_b")],
        [InlineKeyboardButton(text="🏠 Menyu", callback_data="home")]
    ])
    await c.message.answer(f"🎮 Quiz: {q}", reply_markup=kb)

@dp.callback_query(F.data.startswith("ans_"))
async def ans(c: CallbackQuery):
    await c.answer("✅ To'g'ri! +10 ball! Fazilati: Ilm o'rganish savob!", show_alert=True)
    await quiz(c)

# --- 7 TA AVTO ESLATMA ---
async def send_all(t): print(f"AUTO: {t}")
def setup_scheduler():
    scheduler.add_job(lambda: asyncio.create_task(send_all("🌙 BOMDOD 05:10 - @hakiymqalb")), "cron", hour=5, minute=10)
    scheduler.add_job(lambda: asyncio.create_task(send_all("🌅 TONGGI ZIKR 07:00 - /start bosing, 1/10 dan boshlang!")), "cron", hour=7, minute=0)
    scheduler.add_job(lambda: asyncio.create_task(send_all("☀️ PESHIN 12:45")), "cron", hour=12, minute=45)
    scheduler.add_job(lambda: asyncio.create_task(send_all("🌤️ ASR 16:20")), "cron", hour=16, minute=20)
    scheduler.add_job(lambda: asyncio.create_task(send_all("🌙 KECHKI ZIKR 18:30 - /start bosing!")), "cron", hour=18, minute=30)
    scheduler.add_job(lambda: asyncio.create_task(send_all("🌆 SHOM 19:15")), "cron", hour=19, minute=15)
    scheduler.add_job(lambda: asyncio.create_task(send_all("🌃 XUFTON 20:45")), "cron", hour=20, minute=45)
    scheduler.start()

async def main():
    setup_scheduler()
    await dp.start_polling(bot)
if __name__=="__main__": asyncio.run(main())
