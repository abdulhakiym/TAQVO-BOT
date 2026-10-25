import asyncio
import json
import logging
import random
import datetime
import google.generativeai as genai
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart

# === SOZLAMALAR ===
BOT_TOKEN = "8327169780:AAEv-cE8mAB1OhFWTRZ08V9OSbpjDOk7wRA"
GEMINI_API_KEY = "AQ.Ab8RN6I3r2_BMNV6suCzFtUc0euMEYNUCqHkn0gC-OVH0e7xiQ"  # https://aistudio.google.com dan oling - TEKIN!
CHANNEL = "@hakiymqalb"
SITE = "https://abdulhakiym.github.io/TAQVO-BOT/"
USERS_FILE = "users.json"

# GEMINI ULASH
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') # Eng tez va limitsiz model

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def load_users():
    try:
        with open(USERS_FILE, "r") as f: return json.load(f)
    except: return []

def save_user(user_id, name, username):
    users = load_users()
    if not any(u['id'] == user_id for u in users):
        users.append({"id": user_id, "name": name, "username": username})
        with open(USERS_FILE, "w") as f: json.dump(users, f)

async def is_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except: return False

def sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 @hakiymqalb ga obuna bo'lish", url=f"https://t.me/{CHANNEL[1:]}")],
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")]
    ])

def site_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 TAQVO SAYT", url=SITE)]
    ])

DEATH_REMINDERS = [
    "☠️ 'Har bir jon o'limni totib ko'ruvchidir' (Oli Imron, 185)",
    "⚰️ 'Lazzatlarni kesuvchi o'limni ko'p eslang' (Termiziy, sahih)"
]

PRAYER_HADITH = {
    "Bomdod": "Bomdod vaqti! 'Kim Bomdodni jamoat bilan o'qisa...' (Muslim)",
    "Peshin": "Peshin vaqti bo'ldi!",
    "Asr": "Asr vaqti! Asrni tark etgan amali habata bo'ladi (Buxoriy)",
    "Shom": "Shom vaqti!",
    "Xufton": "Xufton vaqti!"
}

@dp.message(CommandStart())
async def start_handler(message: Message):
    name = message.from_user.first_name
    save_user(message.from_user.id, name, message.from_user.username)
    if not await is_sub(message.from_user.id):
        await message.answer(f"Assalamu alaykum va rohmatulloh, {name} aka! 🌸\n\nXush kelibsiz! Alloh iymoningizni salomat qilsin!\n\nKanalga obuna bo'ling:", reply_markup=sub_keyboard())
    else:
        await message.answer(f"Assalamu alaykum va rohmatulloh, {name} aka! Xush kelibsiz! 🕌\n\nAlloh iymoningizni salomat qilsin! Endi har qanday savolingizni yozing - Gemini AI bilan javob beraman!", reply_markup=site_keyboard())

@dp.callback_query(F.data == "check_sub")
async def check_sub_handler(call: CallbackQuery):
    if await is_sub(call.from_user.id):
        await call.message.answer(f"✅ Tasdiqlandi {call.from_user.first_name} aka!", reply_markup=site_keyboard())
        await call.answer("✅ Tasdiqlandi!")
    else:
        await call.answer("❌ Hali obuna emassiz!", show_alert=True)

# === GEMINI BILAN JAVOB BERISH ===
async def ask_gemini(question, user_name):
    prompt = f"""
    Sen TAQVO-BOT san, professional islomiy yordamchisan. Senga {user_name} aka savol beryapti.

    QOIDALAR:
    1. Har doim o'zbek tilida, samimiy, aka-ukadek javob ber
    2. Har qanday savolga javob berasan - diniy, dunyoviy, texnologiya, hayotiy - hammasi
    3. Agar savol islomiy bo'lsa, Qur'on oyati va sahih hadis bilan javob ber
    4. Agar bemani, so'kinish, behayo so'z bo'lsa, qattiq lekin odob bilan Jahannamni va o'limni eslat: "Tahrim surasi 6-oyat..." deb
    5. Oxirida har doim: "☰ Menyuda yoki 🌐 saytda to'liq ma'lumot bor" deb qo'sh
    6. Qisqa, tushunarli, 5-6 qator javob ber, juda uzun qilma

    Savol: {question}
    """
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini error: {e}")
        return f"Kechirasiz {user_name} aka, hozir internetda uzilish bo'ldi. Savolingizni qayta yozib yuboring! 🤲"

@dp.message()
async def ai_handler(message: Message):
    user_id = message.from_user.id
    text = message.text
    text_low = text.lower().strip()
    name = message.from_user.first_name

    if not await is_sub(user_id):
        await message.answer("⛔ Avval @hakiymqalb ga obuna bo'ling!", reply_markup=sub_keyboard())
        return

    # Tez javoblar - internetga bormasdan
    if text_low in ["qalesan", "qalaysan", "qalesiz", "salom", "assalom"]:
        await message.answer(f"Alhamdulillah yaxshi {name} aka! 😊 Siz yaxshimisiz? Nima savolingiz bor?")
        return
    
    if "gusl" in text_low and len(text_low) < 20:
        await message.answer(f"🚿 Gusl: 1.Niyat 2.Avratni yuvish 3.Tahorat 4.Boshga 3 marta suv 5.Butun badan 6.Oyoq. Buxoriy rivoyati. To'liq ☰ Menyuda!")
        return

    # QOLGAN HAMMA SAVOL - GEMINI GA YUBORISH
    await bot.send_chat_action(message.chat.id, "typing")
    answer = await ask_gemini(text, name)
    await message.answer(answer)

async def reminder_loop():
    await asyncio.sleep(10)
    while True:
        try:
            now = datetime.datetime.now()
            hour_min = now.strftime("%H:%M")
            if hour_min in ["05:15", "12:30", "16:15", "18:45", "20:00"]:
                for u in load_users():
                    if await is_sub(u['id']):
                        try: 
                            pname = {"05:15":"Bomdod", "12:30":"Peshin", "16:15":"Asr", "18:45":"Shom", "20:00":"Xufton"}[hour_min]
                            await bot.send_message(u['id'], f"🕌 {PRAYER_HADITH[pname]}\n☰ Menyuda to'liq duo bor!")
                        except: pass
            if hour_min == "06:00":
                for u in load_users():
                    if await is_sub(u['id']):
                        try: await bot.send_message(u['id'], "🌅 Tonggi zikr vaqti! ☰ Menyuda o'qing!", reply_markup=site_keyboard())
                        except: pass
            if hour_min == "18:00":
                for u in load_users():
                    if await is_sub(u['id']):
                        try: await bot.send_message(u['id'], "🌙 Kechki zikr vaqti! ☰ Menyuda o'qing!")
                        except: pass
            if hour_min in ["10:00", "21:00"]:
                for u in load_users():
                    if await is_sub(u['id']):
                        try: await bot.send_message(u['id'], random.choice(DEATH_REMINDERS))
                        except: pass
            await asyncio.sleep(60)
        except: await asyncio.sleep(60)

async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
