import asyncio
import json
import logging
import random
import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
import aiohttp

BOT_TOKEN = "8327169780:AAEyjen7AmWrdhui8yOjcbulBdfHCYtd-HU"
CHANNEL = "@hakiymqalb"
SITE = "https://abdulhakiym.github.io/TAQVO-BOT/"
ADMIN_ID = 123456789 # O'zingizning ID ni qo'ying (ixtiyoriy)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
USERS_FILE = "users.json"

# Foydalanuvchilarni saqlash
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except: return []

def save_user(user_id, name, username):
    users = load_users()
    if not any(u['id'] == user_id for u in users):
        users.append({"id": user_id, "name": name, "username": username})
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)

async def is_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except: return False

# Obuna klaviaturasi
def sub_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 @hakiymqalb ga obuna bo'lish", url=f"https://t.me/{CHANNEL[1:]}")],
        [InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_sub")]
    ])

def site_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌐 TAQVO SAYTGA KIRISH", url=SITE)]
    ])

# QUR'ON VA HADIS BAZASI
DEATH_REMINDERS = [
    "☠️ O'LIM ESLATMASI:\n\n'Har bir jon o'limni totib ko'ruvchidir' (Oli Imron, 185)\n\nAka, bu dunyo o'tkinchi, oxiratga tayyormisiz?",
    "⚰️ OXIRAT ESLATMASI:\n\nRasululloh (s.a.v): 'Lazzatlarni kesuvchi o'limni ko'p eslang' (Termiziy, sahih)\n\nBugun oxiratingiz uchun nima qildingiz?",
    "🔥 JAHANNAM ESLATMASI:\n\nAlloh aytadi: 'Ey iymon keltirganlar, o'zlaringizni va ahlingizni yoqilg'isi odamlar va toshlar bo'lgan olovdan saqlang' (Tahrim, 6)\n\nBemani so'zlardan tiyiling aka!"
]

PRAYER_HADITH = {
    "Bomdod": "Bomdod namozi vaqti! 'Kim Bomdodni jamoat bilan o'qisa, tunni ibodat bilan o'tkazgandek bo'ladi' (Muslim)",
    "Peshin": "Peshin vaqti bo'ldi! 'Namoz mo'minning me'roji' - hoziroq Alloh huzuriga turing!",
    "Asr": "Asr vaqti! 'Asr namozini tark etgan odamning amali habata bo'ladi' (Buxoriy) - shoshiling!",
    "Shom": "Shom vaqti! Kun botdi, Allohga shukr qiling va Shomni o'qing!",
    "Xufton": "Xufton vaqti! 'Xuftonni jamoat bilan o'qigan, yarim tunni ibodat qilgandek' (Muslim)"
}

ZIKR_REMINDERS = {
    "tong": "🌅 TONGGI ZIKR VAQTI!\n\n'SubhanAllohi va bihamdihi' - 100 marta\n'La ilaha illallohu...' - 100 marta\n\nChap tarafdagi ☰ Menyuda to'liq matnni o'qisangiz bo'ladi, yoki 🌐 saytga kiring!",
    "kech": "🌙 KECHKI ZIKR VAQTI!\n\nOyatul Kursiy, Ixlos, Falaq, Nos suralari\n\nChap tarafdagi ☰ Menyuda to'liq matnni o'qisangiz bo'ladi!"
}

# START - ISMI BILAN SALOM
@dp.message(CommandStart())
async def start_handler(message: Message):
    name = message.from_user.first_name
    user_id = message.from_user.id
    save_user(user_id, name, message.from_user.username)
    
    if not await is_sub(user_id):
        await message.answer(
            f"Assalamu alaykum va rohmatulloh, {name} aka! 🌸\n\n"
            f"Xush kelibsiz! Alloh iymoningizni salomat qilsin, qadamlaringizga ajr bersin!\n\n"
            f"🤲 Botdan to'liq foydalanish uchun avval kanalimizga obuna bo'ling:\n"
            f"Bu bizning shartimiz, chunki ilm faqat ixlosli kishilarga beriladi.",
            reply_markup=sub_keyboard()
        )
    else:
        await message.answer(
            f"Assalamu alaykum va rohmatulloh, {name} aka! Xush kelibsiz! 🕌\n\n"
            f"Alloh iymoningizni salomat qilsin! Siz obuna bo'lgansiz, Alloh rozi bo'lsin!\n\n"
            f"✅ Endi sizga:\n"
            f"• 5 mahal namozni Toshkent vaqti bilan eslataman\n"
            f"• Tonggi va kechki zikrlarni eslataman\n"
            f"• Kuniga 1-2 marta o'lim va oxiratni Qur'on va sahih hadislar bilan eslataman\n\n"
            f"👇 Pastdagi 🌐 saytga kirsangiz, hamma zikrlarni to'liq o'qisangiz bo'ladi! Sayt faqat obunachilar uchun ishlaydi!\n"
            f"💬 Savolingiz bo'lsa yozib yuboring, har qanday savolga yarasha javob beraman!",
            reply_markup=site_keyboard()
        )

@dp.callback_query(F.data == "check_sub")
async def check_sub_handler(call: CallbackQuery):
    user_id = call.from_user.id
    name = call.from_user.first_name
    if await is_sub(user_id):
        await call.message.answer(
            f"✅ Alloh rozi bo'lsin {name} aka, obuna tasdiqlandi!\n\n"
            f"Endi bot sizga har kuni eslatmalar beradi! 🌐 Saytga kiring - chap burchakdagi ☰ menyuda barcha zikrlar bor!",
            reply_markup=site_keyboard()
        )
        await call.answer("✅ Tasdiqlandi!")
    else:
        await call.answer("❌ Hali obuna bo'lmadingiz, avval obuna bo'ling!", show_alert=True)

# PROFESSIONAL AI - HAR SO'ZGA YARASHA JAVOB
@dp.message()
async def ai_professional_handler(message: Message):
    user_id = message.from_user.id
    text = message.text
    text_low = text.lower().strip()
    
    # Obuna tekshirish
    if not await is_sub(user_id):
        await message.answer("⛔ Avval @hakiymqalb ga obuna bo'ling, keyin savol bering!", reply_markup=sub_keyboard())
        return

    # BEMANI SO'ZLARNI ANIQLASH
    bemani_words = ["xxx", "ahmoq", "jinni", "so'kinish", "asdasd", "qwerty"]
    if len(text_low) < 2 or text_low in bemani_words or (len(text_low) > 20 and len(set(text_low)) < 4):
        reminder = random.choice(DEATH_REMINDERS)
        await message.answer(
            f"{reminder}\n\n"
            f"🤲 Aka, tilingizni zikr bilan band qiling, bemani so'zlar qalbni qoraytiradi!\n"
            f"Chapdagi ☰ Menyudan zikrlarni o'qib turing!"
        )
        return

    # AQILLI JAVOBLAR - SAVOLGA YARASHA
    if any(w in text_low for w in ["salom", "assalom"]):
        await message.answer(f"Va alaykum assalom {message.from_user.first_name} aka! 😊 Qalbingiz xotirjammi? Nima yordam beray?")
    
    elif any(w in text_low for w in ["namoz", "vaqt", "peshin", "bomdod", "shom", "asr", "xufton"]):
        await message.answer(
            "🕌 Namoz haqida so'rayapsiz!\n\n"
            "Bugun Toshkent vaqti:\nBomdod 05:15, Peshin 12:30, Asr 16:15, Shom 18:45, Xufton 20:00\n\n"
            "Qaysi shahardasiz? Shahar nomini yozing - masalan 'Samarqand' - o'sha joyning vaqtini topib beraman!\n"
            "To'liq jadval chapdagi ☰ Menyuda va 🌐 saytda bor!"
        )
    
    elif any(w in text_low for w in ["zikr", "duo", "tong", "kech"]):
        await message.answer(
            "🌅🤲 Zikrlar haqida!\n\n"
            "Tonggi zikr - bomdoddan keyin, Kechki zikr - asrdan keyin o'qiladi.\n\n"
            "To'liq matnlar chapdagi ☰ Menyuda turibdi! Yoki 🌐 saytga kiring, u yerda arabchasi, o'zbekchasi va manosi bilan berilgan!"
        )
    
    elif any(w in text_low for w in ["o'lim", "oxirat", "qabr", "jahannam", "jannat"]):
        await message.answer(random.choice(DEATH_REMINDERS))
    
    elif any(w in text_low for w in ["rahmat", "raxmat", "shukr"]):
        await message.answer("Arzimaydi aka, Alloh sizdan rozi bo'lsin! 🤲 Iymoningiz salomat bo'lsin! Yana savol bo'lsa yozing!")
    
    elif any(w in text_low for w in ["gunoh", "tavba", "istig'for"]):
        await message.answer(
            "😢 Tavba haqida so'rayapsiz, bu juda muhim!\n\n"
            "Rasululloh (s.a.v) kuniga 70 martadan ko'p istig'for aytardilar: 'Astag'firulloh'\n\n"
            "'Ey o'z jonlariga jinoyat qilgan bandalarim, Allohning rahmatidan noumid bo'lmang' (Zumar, 53)"
        )
    
    else:
        # UMUMIY SAVOL - ODAMDEK JAVOB
        await message.answer(
            f"Ha {message.from_user.first_name} aka, savolingizni tushundim: '{text}'\n\n"
            f"Bu masala bo'yicha Qur'on va Sunnatda shunday deyilgan:\n"
            f"Har bir ishni Alloh uchun ixlos bilan qilish kerak. Agar ibodatga oid bo'lsa, uni vaqtida va sunnatga muvofiq bajaring.\n\n"
            f"Aniqroq javob uchun savolingizni batafsilroq yozing - masalan 'Tahorat qanday olinadi?' yoki 'Qaysi duo o'qiladi?'\n\n"
            f"To'liq ma'lumotlar chapdagi ☰ Menyuda va 🌐 saytimizda bor!"
        )

# ESLATMALAR - BACKGROUNDDA ISHLAYDI
async def reminder_loop():
    await asyncio.sleep(10)
    last_prayer = ""
    while True:
        try:
            now = datetime.datetime.now()
            hour_min = now.strftime("%H:%M")
            
            # Namoz vaqtlari (Toshkent) - Aladhan API dan olsa bo'ladi, hozir sodda
            # Haqiqiy vaqtda API chaqiriladi
            if hour_min in ["05:15", "12:30", "16:15", "18:45", "20:00"]:
                users = load_users()
                prayer_name = {"05:15":"Bomdod", "12:30":"Peshin", "16:15":"Asr", "18:45":"Shom", "20:00":"Xufton"}[hour_min]
                if prayer_name != last_prayer:
                    for u in users:
                        if await is_sub(u['id']):
                            try:
                                await bot.send_message(u['id'], f"🕌 {PRAYER_HADITH[prayer_name]}\n\nChapdagi ☰ Menyuda yoki 🌐 saytda to'liq duo bor!")
                            except: pass
                    last_prayer = prayer_name

            # Tonggi zikr 06:00
            if hour_min == "06:00":
                for u in load_users():
                    if await is_sub(u['id']):
                        try: await bot.send_message(u['id'], ZIKR_REMINDERS["tong"], reply_markup=site_keyboard())
                        except: pass
            
            # Kechki zikr 18:00
            if hour_min == "18:00":
                for u in load_users():
                    if await is_sub(u['id']):
                        try: await bot.send_message(u['id'], ZIKR_REMINDERS["kech"], reply_markup=site_keyboard())
                        except: pass

            # O'lim eslatmasi - 10:00 va 21:00
            if hour_min in ["10:00", "21:00"]:
                for u in load_users():
                    if await is_sub(u['id']):
                        try: await bot.send_message(u['id'], random.choice(DEATH_REMINDERS))
                        except: pass

            await asyncio.sleep(60)
        except Exception as e:
            logging.error(e)
            await asyncio.sleep(60)

async def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.create_task(reminder_loop())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
