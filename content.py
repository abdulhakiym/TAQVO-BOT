"""Eslatma kontenti. MUHIM: raqamlar va matnlarni nashrdan oldin sunnah.com / hadis manbalaridan
tekshiring (men ularni ishga tushirish paytida internetdan solishtira olmadim)."""

# [davlat(uz), davlat(API), usul, Asr maktabi (1=Hanafiy), [[shahar(uz), shahar(API)], ...]]
COUNTRIES = [
    ["O‘zbekiston", "Uzbekistan", 3, 1, [["Toshkent", "Tashkent"], ["Samarqand", "Samarkand"], ["Buxoro", "Bukhara"], ["Andijon", "Andijan"], ["Namangan", "Namangan"], ["Farg‘ona", "Fergana"], ["Qo‘qon", "Kokand"], ["Nukus", "Nukus"], ["Urganch", "Urgench"], ["Xiva", "Khiva"], ["Qarshi", "Karshi"], ["Termiz", "Termez"], ["Jizzax", "Jizzakh"], ["Navoiy", "Navoi"], ["Guliston", "Gulistan"]]],
    ["Qirg‘iziston", "Kyrgyzstan", 3, 1, [["Bishkek", "Bishkek"], ["O‘sh", "Osh"], ["Jalolobod", "Jalal-Abad"], ["Qorako‘l", "Karakol"], ["Norin", "Naryn"], ["Talas", "Talas"]]],
    ["Qozog‘iston", "Kazakhstan", 3, 1, [["Astana", "Astana"], ["Almati", "Almaty"], ["Shimkent", "Shymkent"], ["Turkiston", "Turkistan"], ["Oqtobe", "Aktobe"]]],
    ["Tojikiston", "Tajikistan", 3, 1, [["Dushanbe", "Dushanbe"], ["Xo‘jand", "Khujand"], ["Ko‘lob", "Kulob"], ["Bo‘xtar", "Bokhtar"]]],
    ["Turkmaniston", "Turkmenistan", 3, 1, [["Ashxobod", "Ashgabat"], ["Turkmanobod", "Turkmenabat"], ["Dashog‘uz", "Dashoguz"]]],
    ["Rossiya", "Russia", 14, 1, [["Moskva", "Moscow"], ["Sankt-Peterburg", "Saint Petersburg"], ["Qozon", "Kazan"], ["Ufa", "Ufa"], ["Grozniy", "Grozny"], ["Mahachqal‘a", "Makhachkala"], ["Yekaterinburg", "Yekaterinburg"], ["Novosibirsk", "Novosibirsk"]]],
    ["Turkiya", "Turkey", 13, 1, [["Istanbul", "Istanbul"], ["Anqara", "Ankara"], ["Izmir", "Izmir"], ["Konya", "Konya"]]],
    ["Saudiya Arabistoni", "Saudi Arabia", 4, 0, [["Makka", "Makkah"], ["Madina", "Medina"], ["Ar-Riyod", "Riyadh"]]],
    ["Germaniya", "Germany", 3, 1, [["Berlin", "Berlin"], ["Kyoln", "Cologne"], ["Myunxen", "Munich"]]],
]

PRAYER_NAMES = {"Fajr": "Bomdod", "Dhuhr": "Peshin", "Asr": "Asr", "Maghrib": "Shom", "Isha": "Xufton"}

# Oxirat, o'lim, qiyomat eslatmalari: h = hadis (ma'nosi), q = Qur'on oyati (matni API'dan olinadi)
AKHIRAH = [
    {"t": "h", "text": "Rasululloh ﷺ mening yelkamdan ushlab: “Dunyoda go‘yo g‘arib yoki yo‘lovchidek bo‘l”, dedilar.", "src": "Buxoriy 6416"},
    {"t": "q", "ref": "3:185"},
    {"t": "h", "text": "Ikki ne’mat borki, ko‘p odamlar ularda aldanib qoladi: sog‘lik va bo‘sh vaqt.", "src": "Buxoriy 6412"},
    {"t": "h", "text": "Jannat sizlardan biringizga poyabzalining ipidan ham yaqin, do‘zax ham xuddi shunday.", "src": "Buxoriy 6488"},
    {"t": "q", "ref": "21:35"},
    {"t": "h", "text": "Inson vafot etsa, amali uziladi, faqat uch narsa qoladi: sadaqai joriya, foydali ilm yoki unga duo qiladigan solih farzand.", "src": "Muslim 1631"},
    {"t": "q", "ref": "39:30"},
    {"t": "h", "text": "Dunyo mo‘min uchun zindon, kofir uchun jannatdir.", "src": "Muslim 2956"},
    {"t": "q", "ref": "62:8"},
    {"t": "h", "text": "Qiyomat kuni quyosh odamlarga yaqinlashtiriladi. Ular amallariga qarab terga botadilar: ba’zilarga ter to‘piqqacha, ba’zilarga tizzagacha, ba’zilarga belgacha yetadi, ba’zilarni esa butunlay qamrab oladi.", "src": "Muslim 2864"},
    {"t": "q", "ref": "2:281"},
    {"t": "h", "text": "Alloh o‘z soyasidan boshqa soya bo‘lmaydigan kunda yetti toifani soyasida saqlaydi: adolatli hukmdor; Alloh ibodatida o‘sgan yigit; qalbi masjidlarga bog‘langan kishi; Alloh uchun bir-birini sevib, shu yo‘lda to‘planib, shu yo‘lda ajralgan ikki kishi; mansabdor va go‘zal ayol (harom ishga) chaqirganda “Allohdan qo‘rqaman” degan kishi; o‘ng qo‘li nima berganini chap qo‘li bilmaydigan darajada yashirin sadaqa qilgan kishi; yolg‘iz qolib Allohni eslab, ko‘zlaridan yosh oqqan kishi.", "src": "Buxoriy 660, Muslim 1031"},
    {"t": "q", "ref": "31:33"},
    {"t": "h", "text": "Sizlardan biringiz vafot etsa, ertayu kech unga joyi ko‘rsatib turiladi: jannat ahlidan bo‘lsa jannatdagi, do‘zax ahlidan bo‘lsa do‘zaxdagi joyi. Unga: “Bu Alloh seni qiyomat kuni tiriltirguncha turadigan joying”, deyiladi.", "src": "Buxoriy 1379, Muslim 2866"},
    {"t": "q", "ref": "4:78"},
    {"t": "h", "text": "Kim Allohning huzuriga yo‘liqishni yoqtirsa, Alloh ham uning huzuriga yo‘liqishni yoqtiradi. Kim buni yoqtirmasa, Alloh ham yoqtirmaydi.", "src": "Buxoriy 6507, Muslim 2683"},
    {"t": "q", "ref": "29:57"},
    {"t": "h", "text": "Kim Allohga va oxirat kuniga iymon keltirgan bo‘lsa, yaxshi gapirsin yoki sukut qilsin.", "src": "Buxoriy 6018, Muslim 47"},
    {"t": "q", "ref": "50:19"},
    {"t": "h", "text": "Ikki kalima tilga yengil, mezonda og‘ir, Rahmonga suyukli: “Subhanallohi va bihamdihi, Subhanallohil Azim”.", "src": "Buxoriy 6406, Muslim 2694"},
    {"t": "q", "ref": "18:46"},
    {"t": "q", "ref": "3:30"},
    {"t": "q", "ref": "99:7"},
]

ZIKR_MORNING = [
    {"text": "Kim kuniga yuz marta “Subhanallohi va bihamdihi” desa, gunohlari dengiz ko‘pigicha bo‘lsa ham kechiriladi.",
     "ar": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ", "src": "Buxoriy 6405, Muslim 2691"},
    {"text": "Kim kuniga yuz marta quyidagi zikrni aytsa, o‘nta qul ozod qilgan savobini oladi, unga yuzta yaxshilik yoziladi, yuzta yomonligi o‘chiriladi va o‘sha kuni kechgacha shaytondan himoyada bo‘ladi.",
     "ar": "لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ", "src": "Buxoriy 3293, Muslim 2691"},
    {"text": "Sayyidul istig‘for: kim uni ertalab ishonch bilan aytsa va o‘sha kuni kechgacha vafot etsa, jannat ahlidan bo‘ladi.",
     "ar": "اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ", "src": "Buxoriy 6306"},
    {"text": "Ikki kalima tilga yengil, mezonda og‘ir, Rahmonga suyukli.",
     "ar": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ", "src": "Buxoriy 6406, Muslim 2694"},
]

ZIKR_EVENING = [
    {"text": "Sayyidul istig‘for: kim uni kechqurun ishonch bilan aytsa va o‘sha kecha tong otmay vafot etsa, jannat ahlidan bo‘ladi.",
     "ar": ZIKR_MORNING[2]["ar"], "src": "Buxoriy 6306"},
    {"text": "Uyquga yotganda Oyatul Kursini o‘qisang, Alloh tomonidan senga doimiy himoyachi bo‘ladi va tong otguncha shayton yaqinlasha olmaydi.",
     "ar": "", "src": "Buxoriy 2311"},
    {"text": "Rasululloh ﷺ har kecha to‘shagiga yotganda ikki kaftini jamlab, ularga Ixlos, Falaq va Nos suralarini o‘qib puflar, so‘ng kaftlarini boshidan boshlab tanasiga surtar edilar.",
     "ar": "", "src": "Buxoriy 5017"},
    {"text": "Ikki kalima tilga yengil, mezonda og‘ir, Rahmonga suyukli.",
     "ar": "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ", "src": "Buxoriy 6406, Muslim 2694"},
]
