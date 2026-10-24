import os
import requests
import random
import pytz
from datetime import time
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "hakiymqalb"
CHANNEL_LINK = "https://t.me/hakiymqalb"
TIMEZONE = pytz.timezone("Asia/Almaty")

MORNING_ZIKRS = [
    "1. Асбаҳна ва асбаҳал мулку лиллаҳи, вал ҳамду лиллаҳ, ла илаҳа иллаллоҳу ваҳдаҳу ла шарика лаҳу...\nMa'nosi: Tong ottirdik, mulk Allohniki...",
    "2. Аллоҳумма бика асбаҳна ва бика амсайна...\nMa'nosi: Allohim, Sening irodang bilan tong ottirdik...",
    "3. Субҳаналлоҳи ва биҳамдиҳи - 100 марта\nRasululloh ﷺ: Kim 100 marta aytsa gunohlari dengiz ko'pigidek bo'lsa ham kechiriladi (Buxoriy)",
    "4. Ла илаҳа иллаллоҳу ваҳдаҳу ла шарика лаҳу... - 100 марта\n100 savob, 100 gunoh o'chiriladi, shaytondan himoya (Buxoriy)"
]

EVENING_ZIKRS = [
    "1. Амсайна ва амсал мулку лиллаҳ...\nMa'nosi: Kech kiritdik, mulk Allohniki...",
    "2. Аъузу бикалиматиллаҳит-таммати мин шарри ма холақо - 3 марта\nZararli narsadan himoya (Muslim)",
    "3. Бисмиллаҳиллази ла язурру маъасмиҳи шайъун... - 3 марта\nHech narsa zarar bermaydi (Tirmiziy)",
    "4. Оятал Курсий - Аллоҳу ла илаҳа илла ҳувал ҳаййул қаййум..."
]

AKHIRAT_ESLATMA = [
    "☠️ 'Har bir jon o'limni totib ko'ruvchidir. So'ngra Bizga qaytarilasiz' (Ankabut 57)\nBugun amallar bor, hisob yo'q. Ertaga hisob bor, amal yo'q.",
    "☠️ Qabr - jannat bog'laridan bir bog' yoki jahannam chuqurlaridan bir chuqur. Rasululloh ﷺ: Qabr oxirat manzillarining birinchisidir.",
    "☠️ 'Qayerda bo'lsangiz ham o'lim sizga yetadi, hatto mustahkam qal'alarda bo'lsangiz ham' (Niso 78)\nO'limdan qochib qutula olmaysiz, unga tayyorgarlik ko'ring!",
    "☠️ Bu dunyo o'yin-kulgu va ziynatdan boshqa narsa emas, oxirat esa haqiqiy hayotdir (Ankabut 64)\nOxirat uchun nima tayyorlading?",
    "☠️ Rasululloh ﷺ: 'Lazzatlarni kesuvchi bo'lgan o'limni ko'p eslang' (Tirmiziy). O'limni eslash qalbni yumshatadi, gunohdan qaytaradi."
]

HADISLAR = [
    "📜 Rasululloh ﷺ: 'Amallar niyatlarga bog'liqdir' (Buxoriy, Muslim)\nHar ishni Alloh uchun niyat qiling.",
    "📜 Rasululloh ﷺ: 'Din nasihatdir' (Muslim)\nAllohga, Kitobiga, Payg'ambariga va musulmonlarga nasihat.",
    "📜 'Poklik iymonning yarmidir' (Muslim)\nTahoratga, tozalikka e'tibor bering.",
    "📜 Rasululloh ﷺ: 'Alloh go'zaldir, go'zallikni yaxshi ko'radi' (Muslim)",
    "📜 'Musulmon musulmonning birodaridir, unga zulm qilmaydi' (Buxoriy)"
]

tasbeh_count = {}

async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        if member.status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        print(f"Check error: {e}")
        return True
    keyboard = [
        [InlineKeyboardButton(f"📢 @{CHANNEL_USERNAME} ga obuna bo'lish", url=CHANNEL_LINK)],
        [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_sub")]
    ]
    if update.message:
        await update.message.reply_text(f"⛔ Botdan foydalanish uchun avval kanalimizga obuna bo'ling:\n\n👉 @{CHANNEL_USERNAME}\n\nObuna bo'lgach 'Tekshirish' ni bosing.", reply_markup=InlineKeyboardMarkup(keyboard))
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    keyboard = [
        ["🕌 Namoz vaqtlari", "📿 Tasbeh"],
        ["🌅 Tonggi zikrlar", "🌙 Kechki zikrlar"],
        ["📖 Qur'on o'qish", "📜 Hadis yodlash"],
        ["🧭 Qibla", "☠️ Oxirat eslatmasi"]
    ]
    await update.message.reply_text(f"Assalomu alaykum {update.effective_user.first_name}! 🤲\n\nMen TAQVO-BOT man, @hakiymqalb kanali uchun maxsus:\n\n🕋 Sahih zikrlar, namoz vaqtlari, Qur'on, oxirat eslatmalari bilan qalbingizni poklang.\n\nPastdagi tugmadan birini tanlang:", reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def get_prayer_times():
    try:
        url = "http://api.aladhan.com/v1/timingsByCity?city=Karaganda&country=Kazakhstan&method=2"
        data = requests.get(url, timeout=10).json()
        return data['data']['timings']
    except:
        return None

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_subscription(update, context):
        return
    text = update.message.text
    user_id = update.effective_user.id

    if "Namoz" in text:
        timings = await get_prayer_times()
        if timings:
            msg = f"🕌 Karaganda - Bugungi namoz vaqtlari:\n\n🌅 Bomdod: {timings['Fajr']}\n🌄 Quyosh: {timings['Sunrise']}\n☀️ Peshin: {timings['Dhuhr']}\n🌤️ Asr: {timings['Asr']}\n🌆 Shom: {timings['Maghrib']}\n🌙 Xufton: {timings['Isha']}\n\n📍 @hakiymqalb"
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Hozir yuklanmadi, keyinroq urinib ko'ring.")

    elif "Tasbeh" in text:
        tasbeh_count[user_id] = tasbeh_count.get(user_id, 0) + 1
        await update.message.reply_text(f"📿 {tasbeh_count[user_id]}\n\nSubhanAlloh! Har bosishda savob. Yana bosing!\nTozalash: /reset\n\n@hakiymqalb")

    elif "Tonggi" in text:
        await update.message.reply_text("🌅 Tonggi sahih zikrlar (Sahih hadislardan):\n\n" + "\n\n".join(MORNING_ZIKRS))

    elif "Kechki" in text:
        await update.message.reply_text("🌙 Kechki sahih zikrlar:\n\n" + "\n\n".join(EVENING_ZIKRS))

    elif "Qur'on" in text:
        keyboard = [
            [InlineKeyboardButton("Fotiha (1)", callback_data="surah_1"), InlineKeyboardButton("Ixlos (112)", callback_data="surah_112")],
            [InlineKeyboardButton("Baqara (2)", callback_data="surah_2"), InlineKeyboardButton("Yosin (36)", callback_data="surah_36")],
            [InlineKeyboardButton("Mulk (67)", callback_data="surah_67"), InlineKeyboardButton("Kahf (18)", callback_data="surah_18")]
        ]
        await update.message.reply_text("📖 Qur'on o'qish - Surani tanlang (bot ichida o'qiysiz, tashqariga chiqmaydi):", reply_markup=InlineKeyboardMarkup(keyboard))

    elif "Hadis" in text:
        await update.message.reply_text("📜 Bugungi hadis yodlash:\n\n" + random.choice(HADISLAR) + "\n\n@hakiymqalb da davomi bor")

    elif "Qibla" in text:
        await update.message.reply_text("🧭 Karaganda uchun Qibla yo'nalishi:\n\n📍 Taxminan 215° - Janubi-G'arb\nKa'ba tomon: 21.4225° N, 39.8262° E\n\nJoynamozni shu tomonga qo'ying.\n\nMaslahat: Telefon kompasidan foydalaning.")

    elif "Oxirat" in text:
        await update.message.reply_text(random.choice(AKHIRAT_ESLATMA) + "\n\n@hakiymqalb - qalblar uchun")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check_sub":
        try:
            member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", query.from_user.id)
            if member.status in ['member', 'administrator', 'creator']:
                await query.edit_message_text("✅ Rahmat! Obuna tasdiqlandi. Endi /start bosing va botdan foydalaning.")
            else:
                await query.answer("❌ Hali obuna bo'lmagansiz, avval obuna bo'ling!", show_alert=True)
        except:
            await query.answer("❌ Obuna topilmadi", show_alert=True)
    elif query.data.startswith("surah_"):
        surah_id = query.data.split("_")[1]
        try:
            url = f"https://api.alquran.cloud/v1/surah/{surah_id}/uz.mansour"
            r = requests.get(url, timeout=10).json()
            surah = r['data']
            text = f"📖 {surah['englishName']} ({surah['name']}) - {surah['numberOfAyahs']} oyat:\n\n"
            for ayah in surah['ayahs'][:15]:
                text += f"{ayah['numberInSurah']}. {ayah['text']}\n"
            if len(surah['ayahs']) > 15:
                text += f"\n... davomi {surah['numberOfAyahs']} oyatgacha. To'liq o'qish: @hakiymqalb"
            await query.edit_message_text(text[:4000])
        except Exception as e:
            await query.edit_message_text("Surani yuklashda xatolik, keyinroq urinib ko'ring.")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasbeh_count[update.effective_user.id] = 0
    await update.message.reply_text("📿 Tasbeh tozalandi - 0 dan boshlandi")

def main():
    token = BOT_TOKEN
    if not token:
        print("BOT_TOKEN yo'q!")
        return
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Bot ishga tushdi - @hakiymqalb")
    app.run_polling()

if __name__ == "__main__":
    main()
