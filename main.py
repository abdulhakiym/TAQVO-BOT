import json, time, ssl, urllib.request, urllib.parse
ssl._create_default_https_context = ssl._create_unverified_context

BOT_TOKEN = "YANGI_TOKENINGIZNI_BU_YERGA_QOYING"
CHANNEL = "@hakiymqalb"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"
SITE = "https://abdulhakiym.github.io/TAQVO-BOT/"

def send(method, data=None):
    url = f"{API}/{method}"
    if data: data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=data)
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode())

def is_sub(uid):
    try:
        res = send("getChatMember", {"chat_id": CHANNEL, "user_id": uid})
        return res["result"]["status"] in ("member","administrator","creator")
    except: return False

print("✅ TAQVO BOT ISHGA TUSHDI")
offset=0
while True:
    try:
        ups = send("getUpdates", {"offset": offset, "timeout": 20})
        for up in ups.get("result", []):
            offset = up["update_id"]+1
            msg = up.get("message")
            cq = up.get("callback_query")
            if msg and "text" in msg:
                chat=msg["chat"]["id"]; uid=msg["from"]["id"]; text=msg["text"]
                if text=="/start":
                    if not is_sub(uid):
                        kb={"inline_keyboard":[[{"text":"📢 @hakiymqalb ga obuna","url":"https://t.me/hakiymqalb"}],[{"text":"✅ Tekshirish","callback_data":"check"}]]}
                        send("sendMessage",{"chat_id":chat,"text":"Botni ishlatish uchun kanalga obuna bo'ling:","reply_markup":json.dumps(kb)})
                    else:
                        kb={"inline_keyboard":[
                            [{"text":"📖 600 Siyrat","callback_data":"siyrat"},{"text":"📿 Tasbeh","callback_data":"tasbeh"}],
                            [{"text":"🌅 Tonggi zikr","callback_data":"tong"},{"text":"🌙 Kechki zikr","callback_data":"kech"}],
                            [{"text":"🕌 Namoz vaqtlari","callback_data":"namoz"},{"text":"🏆 Reyting","callback_data":"reyting"}],
                            [{"text":"🤖 TAQVO AI","callback_data":"ai"}],
                            [{"text":"🌐 TAQVO SAYT","web_app":{"url":SITE}}]
                        ]}
                        send("sendMessage",{"chat_id":chat,"text":"🕌 TAQVO BOT\n\n📖 600 Siyrat savoli\n📿 Tasbeh\n🌅 Tonggi zikrlar\n🌙 Kechki zikrlar\n🕌 Namoz vaqtlari\n🏆 Reyting\n🤖 TAQVO AI\n\nTanlang:","reply_markup":json.dumps(kb)})
                else:
                    if not is_sub(uid): continue
                    send("sendMessage",{"chat_id":chat,"text":f"🤖 Savolingiz: {text}\n\nQur'on va Sunnat asosida javob izlang. Aniq fatvo uchun olimga murojaat qiling."})

            if cq:
                chat=cq["message"]["chat"]["id"]; data=cq["data"]; qid=cq["id"]; uid=cq["from"]["id"]
                if data=="check":
                    if is_sub(uid): 
                        send("answerCallbackQuery",{"callback_query_id":qid,"text":"✅ Tasdiqlandi! /start bosing"})
                        send("sendMessage",{"chat_id":chat,"text":"Rahmat! /start bosing"})
                    else: send("answerCallbackQuery",{"callback_query_id":qid,"text":"❌ Hali obuna emassiz","show_alert":True})
                elif data=="namoz":
                    try:
                        ctx=ssl._create_unverified_context()
                        with urllib.request.urlopen("https://api.aladhan.com/v1/timingsByCity?city=Tashkent&country=Uzbekistan&method=2", context=ctx) as r:
                            t=json.loads(r.read())["data"]["timings"]
                            txt=f"🕌 Toshkent namoz vaqtlari:\n\nBomdod: {t['Fajr']}\nPeshin: {t['Dhuhr']}\nAsr: {t['Asr']}\nShom: {t['Maghrib']}\nXufton: {t['Isha']}"
                    except: txt="Vaqtni olishda xato, keyinroq urinib ko'ring"
                    send("sendMessage",{"chat_id":chat,"text":txt})
                elif data=="siyrat": send("sendMessage",{"chat_id":chat,"text":"📖 Siyrat #1: Payg'ambarimiz (s.a.v) Makkada, 571 yilda tug'ilganlar. 40 yoshda payg'ambar bo'lganlar."})
                elif data=="tasbeh": send("sendMessage",{"chat_id":chat,"text":"📿 Tasbeh: SubhanAlloh 33, Alhamdulillah 33, Allohu Akbar 34"})
                elif data=="tong": send("sendMessage",{"chat_id":chat,"text":"🌅 Tonggi zikr: سُبْحَانَ اللهِ وَبِحَمْدِهِ - 100 marta (Buxoriy)"})
                elif data=="kech": send("sendMessage",{"chat_id":chat,"text":"🌙 Kechki zikr: Oyatul Kursiy - Baqara 255 oyat"})
                elif data=="ai": send("sendMessage",{"chat_id":chat,"text":"🤖 TAQVO AI: Savolingizni yozib yuboring, men javob beraman!"})
                elif data=="reyting": send("sendMessage",{"chat_id":chat,"text":"🏆 Reyting: Sizning ballingiz 0. Siyrat savollariga javob berib ball to'plang!"})
    except Exception as e:
        print("Xato:", e); time.sleep(3)
