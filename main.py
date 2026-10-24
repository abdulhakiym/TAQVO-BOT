import os, random, requests, pytz, asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = "hakiymqalb"
CHANNEL_LINK = f"https://t.me/{CHANNEL_USERNAME}"
TIMEZONE = pytz.timezone("Asia/Almaty")

# --- OBUNA TEKSHIRISH ---
async def is_subscribed(user_id, context):
    try:
        m = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return m.status in ["member", "administrator", "creator"]
    except: return False

# --- MA'LUMOTLAR BAZASI ---
MORNING_ZIKRS = [
    {"ar": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ", "uz": "Tong otdirdik, butun mulk Allohnikidir", "faz": "Tongda o'qilsa, kun davomida Alloh himoyasida bo'lasiz"},
    {"ar": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ 100x", "uz": "Allohni poklab hamd aytaman", "faz": "100 marta aytsa, dengiz ko'pigidek gunohlari kechiriladi"},
    {"ar": "اللَّهُمَّ بِكَ أَصْبَحْنَا", "uz": "Allohim, Sening yordaming bilan tong otdirdik", "faz": "Tongi zikrlarning sayyidi"},
]
EVENING_ZIKRS = [
    {"ar": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ", "uz": "Kech kiritdik, mulk Allohnikidir", "faz": "Kechasi yomonliklardan asraydi"},
    {"ar": "آيَةُ الْكُرْسِيّ", "uz": "Oyatal Kursiy - Allohu la ilaha illa huval hayyul qayyum", "faz": "O'qisa tonggacha farishta qo'riqlaydi"},
]
QABIR_ESLATMALAR = [
    "🪦 Bugun yer ustidamiz, ertaga yer ostidamiz... Qabir zulmatidan Alloh asrasin. Astag'firulloh ayting!",
    "💔 O'lim har kuni bizga yaqinlashmoqda. Bugun tavba qilish vaqti emasmi?",
    "🪦 Qabirda birinchi kecha... Yorug'lik faqat amallaringiz bo'ladi. Namozni tark etmang!",
    "☝️ Oxiratni unutgan qalb - o'lik qalbdir. Allohni zikr qiling!",
]

# --- MENULAR ---
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Qur'on Kitob", callback_data="quran"), InlineKeyboardButton("🎧 30 Pora Audio", callback_data="quran_audio")],
        [InlineKeyboardButton("📚 Sahih Hadislar", callback_data="hadis")],
        [InlineKeyboardButton("🌅 Tongi Zikr", callback_data="tong"), InlineKeyboardButton("🌙 Kechgi Zikr", callback_data="kech")],
        [InlineKeyboardButton("🪦 Qabir/Oxirat", callback_data="qabir"), InlineKeyboardButton("📿 Tasbeh", callback_data="tasbeh")],
        [InlineKeyboardButton("🕋 Namoz Vaqti", callback_data="namoz"), InlineKeyboardButton("⏰ Eslatmalar", callback_data="eslatma")],
        [InlineKeyboardButton("📢 @hakiymqalb", url=CHANNEL_LINK)]
    ])

def audio_30_menu():
    kb = []; row = []
    for i in range(1, 31):
        row.append(InlineKeyboardButton(f"{i}", callback_data=f"pora_{i}"))
        if len(row) == 5: kb.append(row); row = []
    if row: kb.append(row)
    kb.append([InlineKeyboardButton("🔙 Bosh Menyu", callback_data="back_main")])
    return InlineKeyboardMarkup(kb)

def player_menu(cur):
    prev_n = cur-1 if cur>1 else 30
    next_n = cur+1 if cur<30 else 1
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(f"⏮ {prev_n}-pora", callback_data=f"pora_{prev_n}"), InlineKeyboardButton(f"{next_n}-pora ⏭", callback_data=f"pora_{next_n}")],
        [InlineKeyboardButton("📜 Ro'yxat", callback_data="quran_audio"), InlineKeyboardButton("🔙 Menyu", callback_data="back_main")]
    ])

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_subscribed(user_id, context):
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 @hakiymqalb ga obuna bo'lish", url=CHANNEL_LINK)],
            [InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_sub")]
        ])
        await update.message.reply_text(f"🤲 Botdan foydalanish uchun avval obuna bo'ling:\n👉 @{CHANNEL_USERNAME}", reply_markup=kb)
        return
    await update.message.reply_text(f"🤲 Assalomu alaykum {update.effective_user.first_name}!\n\n🕌 <b>TAQVO BOT - Professional</b>\nQalbingiz xotirjamligi uchun\n\nQuyidan tanlang:", reply_markup=main_menu(), parse_mode="HTML")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    data = q.data; chat_id = q.message.chat_id

    if data == "check_sub":
        if await is_subscribed(q.from_user.id, context):
            await q.message.delete()
            await q.message.reply_text("✅ Obuna tasdiqlandi!", reply_markup=main_menu())
        else: await q.answer("❌ Hali obuna bo'lmadingiz!", show_alert=True)
        return

    if data == "quran":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("Fotiha", callback_data="surah_1"), InlineKeyboardButton("Yosin", callback_data="surah_36")],
            [InlineKeyboardButton("Mulk", callback_data="surah_67"), InlineKeyboardButton("Rohman", callback_data="surah_55")],
            [InlineKeyboardButton("Ixlos", callback_data="surah_112"), InlineKeyboardButton("Falaq,Nos", callback_data="surah_113")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]
        ])
        await q.message.reply_text("📖 Qur'oni Karim - Kitob shaklida sura tanlang:", reply_markup=kb)

    elif data.startswith("surah_"):
        sura = data.split("_")[1]
        await q.message.reply_text(f"📖 {sura}-sura\n\nArabic: بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ\nUzbek: Mehribon va Rahmli Alloh nomi bilan\n\nDavomi tez kunda to'liq qo'shiladi...", reply_markup=main_menu())

    elif data == "quran_audio":
        await q.message.reply_text("🎧 <b>Shayx Yosir Ad-Dosariy - 30 Pora</b>\n\nPorani tanlang, shu yerda eshitasiz:", reply_markup=audio_30_menu(), parse_mode="HTML")

    elif data.startswith("pora_"):
        pora = int(data.split("_")[1])
        audio_url = f"https://server11.mp3quran.net/dosari/{pora:03d}.mp3"
        await q.answer(f"🎧 {pora}-pora yuklanmoqda...")
        try:
            await context.bot.send_audio(chat_id=chat_id, audio=audio_url,
                caption=f"🎧 <b>{pora}-pora - Shayx Ad-Dosariy</b>\n🕌 Bot ichida eshiting\n@hakiymqalb", 
                title=f"{pora}-pora", performer="Yasir Ad-Dosariy", parse_mode="HTML", reply_markup=player_menu(pora))
        except:
            await q.message.reply_text("Audio yuklashda xatolik, qaytadan urinib ko'ring", reply_markup=audio_30_menu())

    elif data == "hadis":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("📗 Sahih Buxoriy", callback_data="buxoriy")],
            [InlineKeyboardButton("📘 Sahih Muslim", callback_data="muslim")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="back_main")]
        ])
        await q.message.reply_text("📚 Sahih Hadislar To'plami:", reply_markup=kb)

    elif data == "buxoriy":
        await q.message.reply_text("📗 <b>Sahih Buxoriy 1-hadis</b>\n\nArabic: إِنَّمَا الأَعْمَالُ بِالنِّيَّاتِ\nUzbek: Amallar niyatga bog'liq\nFazilat: Ixlos bilan qilingan oz amal ham katta ajr", parse_mode="HTML", reply_markup=main_menu())

    elif data == "tong":
        for z in MORNING_ZIKRS:
            await context.bot.send_message(chat_id, f"🌅 <b>Tongi Zikr</b>\n\nArabic: {z['ar']}\nUzbek: {z['uz']}\nFazilat: {z['faz']}", parse_mode="HTML")
        await q.message.reply_text("Yuqoridagi zikrlarni o'qing 👆", reply_markup=main_menu())

    elif data == "kech":
        for z in EVENING_ZIKRS:
            await context.bot.send_message(chat_id, f"🌙 <b>Kechgi Zikr</b>\n\nArabic: {z['ar']}\nUzbek: {z['uz']}\nFazilat: {z['faz']}", parse_mode="HTML")
        await q.message.reply_text("Yuqoridagi zikrlarni o'qing 👆", reply_markup=main_menu())

    elif data == "qabir":
        await q.message.reply_text(f"{random.choice(QABIR_ESLATMALAR)}\n\n🤲 Alloh barchamizni kechirsin!", reply_markup=main_menu())

    elif data == "tasbeh":
        await q.message.reply_text("📿 <b>Tasbeh</b>\n\nSubhanAlloh (33x)\nAlhamdulillah (33x)\nAllohu Akbar (34x)\n\nHar birida jannatda daraxt ekiladi!", parse_mode="HTML", reply_markup=main_menu())

    elif data == "namoz":
        try:
            r = requests.get("http://api.aladhan.com/v1/timingsByCity?city=Karaganda&country=Kazakhstan&method=2").json()
            t = r['data']['timings']
            await q.message.reply_text(f"🕋 <b>Karaganda - Namoz vaqtlari</b>\n\n🌙 Bomdod: {t['Fajr']}\n☀️ Peshin: {t['Dhuhr']}\n⛅ Asr: {t['Asr']}\n🌇 Shom: {t['Maghrib']}\n🌃 Xufton: {t['Isha']}\n\n@hakiymqalb", parse_mode="HTML", reply_markup=main_menu())
        except:
            await q.message.reply_text("Xatolik, keyinroq urinib ko'ring", reply_markup=main_menu())

    elif data == "eslatma":
        await q.message.reply_text("⏰ <b>Eslatmalar</b>\n\n✅ Namoz vaqti eslatmasi: Yoqilgan (tez kunda)\n✅ Tongi zikr 06:00\n✅ Kechgi zikr 19:00\n✅ Qabir eslatmasi kuniga 1 marta\n\nBular avtomatik ishlaydi!", parse_mode="HTML", reply_markup=main_menu())

    elif data == "back_main":
        await q.message.delete()
        await context.bot.send_message(chat_id, "Bosh Menyu:", reply_markup=main_menu())

# --- ISHGA TUSHIRISH ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("TAQVO BOT Professional ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
