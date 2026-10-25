import os, json, random, asyncio, logging
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@hakiymqalb"
SITE = "https://abdulhakiym.github.io/TAQVO-BOT/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
TZ = pytz.timezone("Asia/Tashkent")
scheduler = AsyncIOScheduler(timezone=TZ)

# --- SAQLASH ---
USERS_FILE = "users.json"
SCORES_FILE = "scores.json"
def load_json(f, default): 
    try:
        with open(f, "r") as file: return json.load(file)
    except: return default
def save_json(f, data):
    with open(f, "w") as file: json.dump(data, file)
users = set(load_json(USERS_FILE, []))
scores = load_json(SCORES_FILE, {})

# --- MA'LUMOTLAR ---
SIYRAT = [
    {"q": "Payg'ambarimiz (s.a.v) qayerda tug'ilganlar?", "a": "Makka", "opts": ["Makka","Madina","Toif"]},
    {"q": "Hiro g'orida necha yoshda vahiy kelgan?", "a": "40 yosh", "opts": ["40 yosh","25 yosh","63 yosh"]},
    {"q": "Qur'on necha yilda nozil bo'lgan?", "a": "23 yil", "opts": ["23 yil","10 yil","13 yil"]},
]
OXIRAT = [
    "☝️ ОХИРАТ ЭСЛАТМАСИ:\n\n«Ҳар бир жон ўлимни татиб кўргувчидир» (Оли Имрон, 185)\n\nБу ҳаёт ўткинчи! Охиратга тайёрмисиз?",
    "💀 ЎЛИМ ЭСЛАТМАСИ:\n\n«Қаерда бўлсангиз ҳам ўлим сизни топади» (Нисо, 78)\n\nРасулуллоҳ (с.а.в): «Лаззатларни кесувчи ўлимни кўп эсланг» (Тирмизий, саҳиҳ)",
    "📖 «Ва Охират яхшироқ ва боқийроқдир» (Аъло, 17)\n\nДунё ўйин-кулги эмас, охиратга заҳира йиғинг!",
]
NAMOZ_MATN = {
    "Bomdod": "🌅 БОМДОД вақти бўлди! Тур, таҳорат ол! «Намоз мўминнинг меърожидир» - Намозга шошил!",
    "Peshin": "☀️ ПЕШИН вақти кирди! Ишингизни тўхтатиб Роббингизга юзланинг!",
    "Asr": "🌤️ АСР вақти! «Аср намозини ўтказганнинг амали ҳавода» (Бухорий) - Ўқиб олинг!",
    "Shom": "🌇 ШОМ вақти! Кун ботди, Аллоҳга ҳамд айтиб намозга киришинг!",
    "Xufton": "🌙 ХУФТОН вақти! Кечани намоз билан якунланг, Аллоҳ гуноҳларингизни кечиради!",
}
ISLOMIY_KALIT = ["namoz","tahorat","ro'za","zakot","haj","qur'on","quron","hadis","sunnat","payg'ambar","alloh","islom","fiqh","aqida","siyrat","zikr","duo","halol","harom","nikoh","jannat","jahannam","farz","gunoh","tavba","bomdod","peshin","asr","shom","xufton","vohib","olim"]
BEMANI_JAVOB = [
    "☝️ Аллоҳдан қўрқинг!\n\n«Эй иймон келтирганлар! Аллоҳдан қўрқинглар» (Ҳашр, 18)\n\nВақтингизни бемаъни нарсаларга сарфламанг!",
    "📖 «Мўминлар беҳуда сўздан юз ўгиради» (Мўминун, 3)\n\nМен фақат Исломий мавзуда жавоб бераман! Намоз, рўза, таҳорат ҳақида сўранг!",
]

def is_islamic(q): return any(k in q.lower() for k in ISLOMIY_KALIT)

async def is_sub(uid):
    try: m = await bot.get_chat_member(chat_id=CHANNEL, user_id=uid); return m.status in ("member","administrator","creator")
    except: return False

def sub_kb(): return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📢 @hakiymqalb га обуна", url="https://t.me/hakiymqalb")],[InlineKeyboardButton(text="✅ Текшириш", callback_data="check")]])
def main_kb(): return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📖 600 Сийрат", callback_data="siyrat"), InlineKeyboardButton(text="📿 Тасбеҳ", callback_data="tasbeh")],
    [InlineKeyboardButton(text="🌅 Тонгги зикр", callback_data="tong"), InlineKeyboardButton(text="🌙 Кечки зикр", callback_data="kech")],
    [InlineKeyboardButton(text="🕌 Намоз вақтлари", callback_data="namoz"), InlineKeyboardButton(text="🏆 Рейтинг", callback_data="reyting")],
    [InlineKeyboardButton(text="🤖 ТАҚВО AI га савол", callback_data="ai")],
    [InlineKeyboardButton(text="🌐 САЙТГА КИРИШ", web_app=WebAppInfo(url=SITE))],
])

@dp.message(Command("start"))
async def start(m: types.Message):
    if not await is_sub(m.from_user.id):
        await m.answer(f"Ассалому алайкум, {m.from_user.first_name}! 🕌\n\nМен **ТАҚВО БОТ** ман!\n\nСайтимда нималар бор:\n✅ 600 та Сийрат саволлари\n✅ Тасбеҳ ҳисоблагич\n✅ Тонгги/Кечки зикрлар (чап менюда)\n✅ Намоз вақтлари\n\nБотнинг вазифаси:\n📖 Ҳар куни 1-2 марта Охират/Ўлимни эслатиш (Қуръон ва саҳиҳ ҳадис)\n🕌 Ҳар намоз вақтида эслатиш\n🌅 Тонгги/Кечки зикрларни ўз вақтида эслатиш\n🤖 Исломий AI билан суҳбат\n\n⚠️ **Буларнинг ҳаммаси ва сайтга кириш учун каналимга обуна бўлишинг шарт:**", reply_markup=sub_kb())
    else:
        users.add(m.from_user.id); save_json(USERS_FILE, list(users))
        await m.answer(f"Ва алайкум ассалом, {m.from_user.first_name}! 😊\n\nОбуна тасдиқланди! Бот ишга тушди!\n\n🌐 Сайтга киринг, у ерда барча маълумотлар бор!\n👇 Пастдаги тугмалардан танланг, ёки Исломий саволингизни ёзиб юборинг!", reply_markup=main_kb())

@dp.callback_query(F.data=="check")
async def check(c: types.CallbackQuery):
    if await is_sub(c.from_user.id):
        users.add(c.from_user.id); save_json(USERS_FILE, list(users))
        await c.answer("✅ Тасдиқланди!"); await c.message.answer("✅ Баракалла! Энди бот ва сайт тўлиқ ишлайди!", reply_markup=main_kb())
    else: await c.answer("❌ Ҳали обуна эмассиз!", show_alert=True)

@dp.callback_query(F.data=="siyrat")
async def siyrat_h(c: types.CallbackQuery):
    if not await is_sub(c.from_user.id): return await c.answer("Обуна бўлинг!", show_alert=True)
    s = random.choice(SIYRAT)
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=o, callback_data=f"ans_{o}_{s['a']}")] for o in s["opts"]])
    await c.message.answer(f"📖 Сийрат: {s['q']}", reply_markup=kb)

@dp.callback_query(F.data.startswith("ans_"))
async def ans_h(c: types.CallbackQuery):
    _, tan, togri = c.data.split("_", 2)
    uid = str(c.from_user.id)
    if tan == togri:
        scores[uid] = scores.get(uid, 0) + 10; save_json(SCORES_FILE, scores)
        await c.message.answer(f"✅ Тўғри! +10 балл. Балл: {scores[uid]}", reply_markup=main_kb())
    else: await c.message.answer(f"❌ Нотўғри. Тўғриси: {togri}", reply_markup=main_kb())
    await c.answer("")

@dp.callback_query(F.data=="tasbeh")
async def tasbeh_h(c: types.CallbackQuery): await c.message.answer("📿 Тасбеҳ: Субҳаналлоҳ 33, Алҳамдулиллаҳ 33, Аллоҳу Акбар 34\n\nСайтда ҳисоблагич бор!", reply_markup=main_kb())
@dp.callback_query(F.data=="tong")
async def tong_h(c: types.CallbackQuery): await c.message.answer("🌅 Тонгги зикрлар (06:00):\n\nЧап менюда «Тонгги зикрлар» бўлимида тўлиқ матн бор! Ҳар куни ўқинг!\n\nСубҳаналлоҳи ва биҳамдиҳи 100 марта", reply_markup=main_kb())
@dp.callback_query(F.data=="kech")
async def kech_h(c: types.CallbackQuery): await c.message.answer("🌙 Кечки зикрлар (18:00):\n\nЧап менюда «Кечки зикрлар»да тўлиқ матн бор!\n\nОятул Курсий ва охирги 2 оятни ўқинг!", reply_markup=main_kb())
@dp.callback_query(F.data=="namoz")
async def namoz_h(c: types.CallbackQuery): await c.message.answer("🕌 Тошкент намоз вақтларини мен сизга ҳар намозда эслатаман!", reply_markup=main_kb())
@dp.callback_query(F.data=="reyting")
async def reyting_h(c: types.CallbackQuery):
    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
    txt = "🏆 Рейтинг TOP-10:\n\n" + "\n".join([f"{i}. ID {k} - {v} балл" for i,k,v in enumerate(top,1)]) if top else "Ҳали балл йўқ. Сийратдан бошланг!"
    await c.message.answer(txt, reply_markup=main_kb())
@dp.callback_query(F.data=="ai")
async def ai_h(c: types.CallbackQuery): await c.message.answer("🤖 ТАҚВО AI:\n\nИсломий саволингизни ёзинг! Масалан: «Намоз қандай ўқилади?»\n\nБемаъни савол берсангиз, Аллоҳдан қўрқишга чақираман!")

@dp.message()
async def ai_all(m: types.Message):
    if not await is_sub(m.from_user.id): await m.answer("Аввал обуна бўлинг! /start"); return
    q = m.text
    # AI MANTIĞI
    if not is_islamic(q) and len(q) < 40:
        # Bema'ni deb topilsa
        if any(x in q.lower() for x in ["kino","musiqa","qiz","sevgi","pul","o'yin","salom","qalay","nima gap"]):
            await m.answer(random.choice(BEMANI_JAVOB), reply_markup=main_kb()); return

    # Islomiy javob
    ql = q.lower()
    if "namoz" in ql: ans = "🕌 Намоз: «Албатта намоз вақти белгиланган фарздир» (Нисо, 103). 5 маҳал фарз. Таҳорат билан ўқилади."
    elif "tahorat" in ql: ans = "💧 Таҳорат: Моида сураси 6-оят. Юз, қўл, бошга масҳ, оёқ - фарзлари."
    elif "ro'za" in ql or "ruza" in ql: ans = "🌙 Рўза: «Сизларга рўза фарз қилинди» (Бақара, 183). Исломнинг 3-устуни."
    else: ans = f"🤖 Саволингиз: {q}\n\n📖 Қуръон: «Мен жин ва инсни фақат ибодат учун яратдим» (Зориёт, 56)\n\nҲадис: «Илм олиш ҳар бир мусулмонга фарз» (Ибн Можа, саҳиҳ)\n\nТўлиқ жавоб учун ишончли олимга мурожаат қилинг, мен эслатма бердим!"
    await m.answer(ans, reply_markup=main_kb())

# --- AVTO ESLATMALAR ---
async def send_all(t):
    for uid in list(users):
        try:
            if await is_sub(uid): await bot.send_message(uid, t)
        except: pass
        await asyncio.sleep(0.05)

async def oxirat_job(): await send_all(random.choice(OXIRAT))
async def namoz_job(n): await send_all(f"{NAMOZ_MATN[n]}\n\n📢 @{CHANNEL[1:]}")
async def zikr_job(q):
    if q=="tong": await send_all("🌅 ТОНГГИ ЗИКР вақти!\n\nЧап менюдаги «Тонгги зикрлар»ни ўқиш вақти! Субҳаналлоҳи ва биҳамдиҳи 100 марта")
    else: await send_all("🌙 КЕЧКИ ЗИКР вақти!\n\nЧап менюдаги «Кечки зикрлар»ни ўқиш вақти! Оятул Курсийни ўқинг!")

async def main():
        await bot.delete_webhook(drop_pending_updates=True)
    scheduler.add_job(oxirat_job, "cron", hour=9, minute=0)
    scheduler.add_job(oxirat_job, "cron", hour=20, minute=30)
    scheduler.add_job(namoz_job, "cron", hour=5, minute=15, args=["Bomdod"])
    scheduler.add_job(namoz_job, "cron", hour=12, minute=35, args=["Peshin"])
    scheduler.add_job(namoz_job, "cron", hour=15, minute=50, args=["Asr"])
    scheduler.add_job(namoz_job, "cron", hour=18, minute=25, args=["Shom"])
    scheduler.add_job(namoz_job, "cron", hour=19, minute=45, args=["Xufton"])
    scheduler.add_job(zikr_job, "cron", hour=6, minute=0, args=["tong"])
    scheduler.add_job(zikr_job, "cron", hour=18, minute=0, args=["kech"])
    scheduler.start()
    print("✅ TAQVO FINAL BOT ISHGA TUSHDI")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
