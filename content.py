"""TAQVO BOT ma'lumotlar bazasi.

Turlar:  h = hadis (faqat Sahihayn: Buxoriy va Muslim; matn ma'nosi o'zbekchada)
         q = Qur'on oyati (arabcha matn va o'zbekcha tarjima Qur'on API'sidan olinadi, o'zgartirilmaydi)
         w = "yurakka so'z": oddiy eslatma, hadis yoki oyat DEB KO'RSATILMAYDI

MUHIM: hadis raqamlarini nashrdan oldin sunnah.com / ishonchli hadis kitobidan tekshiring
(men ularni internetdan solishtira olmadim). Xato topsangiz, shu faylda to'g'rilang.
Yangi element qo'shish: tegishli ro'yxatga H(...), Q(...) yoki W(...) qatorini qo'shing.
"""
import random

H = lambda text, src: {"t": "h", "text": text, "src": src}
Q = lambda ref: {"t": "q", "ref": ref}
W = lambda text: {"t": "w", "text": text}

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

# ------------------------------------------------------------------ OXIRAT ESLATMALARI
_HADITH = [
    H("Amallar niyatlarga bog‘liqdir. Har kishiga faqat niyat qilgani bor.", "Buxoriy 1, Muslim 1907"),
    H("Rasululloh ﷺ mening yelkamdan ushlab: “Dunyoda go‘yo g‘arib yoki yo‘lovchidek bo‘l”, dedilar.", "Buxoriy 6416"),
    H("Ikki ne’mat borki, ko‘p odamlar ularda aldanib qoladi: sog‘lik va bo‘sh vaqt.", "Buxoriy 6412"),
    H("Jannat sizlardan biringizga poyabzalining ipidan ham yaqin, do‘zax ham xuddi shunday.", "Buxoriy 6488"),
    H("Inson vafot etsa, amali uziladi, faqat uch narsa qoladi: sadaqai joriya, foydali ilm yoki unga duo qiladigan solih farzand.", "Muslim 1631"),
    H("Dunyo mo‘min uchun zindon, kofir uchun jannatdir.", "Muslim 2956"),
    H("Qiyomat kuni quyosh odamlarga yaqinlashtiriladi. Ular amallariga qarab terga botadilar: ba’zilarga ter to‘piqqacha, ba’zilarga tizzagacha, ba’zilarga belgacha yetadi, ba’zilarni esa butunlay qamrab oladi.", "Muslim 2864"),
    H("Alloh o‘z soyasidan boshqa soya bo‘lmaydigan kunda yetti toifani soyasida saqlaydi: adolatli hukmdor; Alloh ibodatida o‘sgan yigit; qalbi masjidlarga bog‘langan kishi; Alloh uchun bir-birini sevib, shu yo‘lda to‘planib, shu yo‘lda ajralgan ikki kishi; mansabdor va go‘zal ayol (harom ishga) chaqirganda “Allohdan qo‘rqaman” degan kishi; o‘ng qo‘li nima berganini chap qo‘li bilmaydigan darajada yashirin sadaqa qilgan kishi; yolg‘iz qolib Allohni eslab, ko‘zlaridan yosh oqqan kishi.", "Buxoriy 660, Muslim 1031"),
    H("Sizlardan biringiz vafot etsa, ertayu kech unga joyi ko‘rsatib turiladi: jannat ahlidan bo‘lsa jannatdagi, do‘zax ahlidan bo‘lsa do‘zaxdagi joyi. Unga: “Bu Alloh seni qiyomat kuni tiriltirguncha turadigan joying”, deyiladi.", "Buxoriy 1379, Muslim 2866"),
    H("Kim Allohning huzuriga yo‘liqishni yoqtirsa, Alloh ham uning huzuriga yo‘liqishni yoqtiradi. Kim buni yoqtirmasa, Alloh ham yoqtirmaydi.", "Buxoriy 6507, Muslim 2683"),
    H("Kim Allohga va oxirat kuniga iymon keltirgan bo‘lsa, yaxshi gapirsin yoki sukut qilsin.", "Buxoriy 6018, Muslim 47"),
    H("Ikki kalima tilga yengil, mezonda og‘ir, Rahmonga suyukli: “Subhanallohi va bihamdihi, Subhanallohil Azim”.", "Buxoriy 6406, Muslim 2694"),
    H("Qiyomat kuni odamlar yalangoyoq, yalang‘och va xatnasiz to‘planadilar.", "Buxoriy 6527, Muslim 2859"),
    H("O‘zingizdan pastdagilarga qaranglar, yuqoridagilarga qaramanglar. Shunday qilsangiz, Allohning sizga bergan ne’matini kamsitmaysiz.", "Muslim 2963"),
    H("Banda: “Mening molim, mening molim”, deydi. Holbuki uning molidan faqat uch narsa o‘ziniki: yeb tugatgani, kiyib eskirtgani va sadaqa qilib oldindan yuborgani. Qolgani ketuvchi va odamlarga qoldiriladigandir.", "Muslim 2959"),
    H("Allohga qasamki, men kuniga yetmish martadan ko‘proq Allohdan mag‘firat so‘rayman va Unga tavba qilaman.", "Buxoriy 6307"),
    H("Ey odamlar, Allohga tavba qilinglar! Men kuniga yuz marta Unga tavba qilaman.", "Muslim 2702"),
    H("Alloh bandasining tavbasidan, cho‘lda tuyasini yo‘qotib, so‘ng topib olgan kishining shodligidan ham ko‘proq xursand bo‘ladi.", "Buxoriy 6308, Muslim 2744"),
    H("Alloh rahmatni yuz qismga bo‘ldi. To‘qson to‘qqizini O‘zida olib qoldi, bittasini yerga tushirdi. Mahluqotlar bir-biriga rahm qilishi shu bir qism tufaylidir, hatto ot bolasiga zarar yetmasin deb tuyog‘ini ko‘tarib turadi.", "Buxoriy 6000, Muslim 2752"),
    H("Sizlardan biringiz o‘zi uchun yoqtirganni birodari uchun ham yoqtirmaguncha iymon keltirmagan bo‘ladi.", "Buxoriy 13, Muslim 45"),
    H("Kuchli polvon kurashda yengadigan emas. Haqiqiy kuchli — g‘azab paytida o‘zini tuta oladigan kishidir.", "Buxoriy 6114, Muslim 2609"),
    H("Kim bir mo‘minning dunyo tashvishlaridan birini ketkazsa, Alloh uning qiyomat kuni tashvishlaridan birini ketkazadi. Kim qiyinchilikdagi kishiga yengillik qilsa, Alloh dunyo va oxiratda unga yengillik qiladi.", "Muslim 2699"),
    H("Yarim xurmo bilan bo‘lsa ham o‘zingizni do‘zaxdan saqlang.", "Buxoriy 1417, Muslim 1016"),
    H("Sadaqa molni kamaytirmaydi. Kechirimli bo‘lgan bandaning izzatini Alloh oshiradi. Kim Alloh uchun kamtarlik qilsa, Alloh uni ko‘taradi.", "Muslim 2588"),
    H("Zulmdan saqlaninglar, chunki zulm qiyomat kuni zulmatlardir.", "Buxoriy 2447, Muslim 2579"),
    H("Mo‘min mo‘minga bir-birini mustahkamlab turuvchi bino kabidir.", "Buxoriy 481, Muslim 2585"),
    H("Birovning eshigi oldida daryo oqib tursa va u har kuni besh marta unda yuvinsa, tanasida kir qoladimi? Besh vaqt namoz ham xatolarni shunday yuvib ketadi.", "Buxoriy 528, Muslim 667"),
    H("Alloh sizlarning suratlaringiz va molingizga emas, qalblaringiz va amallaringizga qaraydi.", "Muslim 2564"),
    H("Qiyomat kuni odamlar orasida dastlab hukm qilinadigan narsa to‘kilgan qonlardir.", "Buxoriy 6533, Muslim 1678"),
]

_AYAT = [Q(r) for r in (
    "2:197", "2:281", "3:30", "3:102", "3:133", "3:185", "4:78", "6:32", "6:162", "16:96", "17:36", "18:46",
    "18:49", "19:95", "21:1", "21:35", "21:47", "22:1", "23:115", "26:88", "29:57", "31:33", "35:5", "39:30",
    "39:53", "40:39", "50:19", "50:22", "55:26", "56:60", "57:16", "57:20", "59:18", "62:8", "63:9", "67:2",
    "74:38", "82:6", "84:6", "89:27", "99:7", "99:8", "102:1", "102:2", "94:5")]

# Yurakka so'z: hadis yoki oyat emas, shaxsiy eslatma. Matn bazaga ochiq qo'shiladi.
_WORDS = [W(t) for t in (
    "Qabrga hech kim sen bilan birga kirmaydi. Faqat amalingning o‘zi.",
    "Bugun yana bir kun umringdan kamaydi. Uni nimaga almashtirding?",
    "Dunyoning ishlari tugamaydi, lekin sening umring tugaydi.",
    "Janoza ko‘targan qo‘llar bir kun seni ham ko‘taradi. Tayyormisan?",
    "Telefoningda yuzlab kontakt bor. Qabrda esa amalingdan boshqa hamrohing bo‘lmaydi.",
    "Sen kechiktirayotgan tavba, birovning oxirgi nafasi bo‘lishi mumkin. Bugun qaytgin.",
    "Eng yaqining ham seni tuproqqa topshirib qaytadi. Sening yo‘ldoshing — qilgan ishlaring.",
    "Uy qurding, mol topding. Eng muhim uyni, qabringni nima bilan obod qilding?",
    "Hech kim “ertaga”ga kafil emas. Yaxshilikni bugun qil, gunohni bugun tark et.",
    "Qalbing qotib qolganidan qo‘rq. U yig‘lamay qo‘yganda ham Alloh eshigi ochiq, faqat kirishni kechiktirma.",
    "Namozni “keyinroq” deb kechiktirgan har daqiqang uchun javob beradigan kun bor.",
    "Odamlarga yoqish uchun yashama. Allohga yoqish uchun yasha, qolganini U o‘zi to‘g‘rilaydi.",
    "Bugun kimningdir ketganini eshitding. Ketuvchilar navbatida sen ham borsan.",
    "Gunohlaringning soniga emas, Rabbingning rahmati qanchalik keng ekaniga qara. Lekin qaytishni kechiktirma.",
    "Eng og‘ir yuk — ado qilinmagan haqlar. Bugun kimdan kechirim so‘rashing kerak?",
    "Ertalab ko‘zingni ochding. Ba’zilarga bu nasib bo‘lmadi. Shukr qil va kunni qadrla.",
    "Hamma ishga “vaqtim yo‘q” deding. Qabr uchun vaqt topdingmi?",
    "Chiroyli kiyim, chiroyli uy: hammasi qolib ketadi. Olib ketadigan yagona boylik — qalbing va amalingdir.",
    "Bir kun kelib hamma narsa jim bo‘ladi. Shu jimlikdan oldin tilingni zikr bilan hayotga qaytar.",
    "Yig‘lay olmayotgan bo‘lsang, o‘zingni Allohdan uzoq deb hisoblama. Duo qilib ko‘r, yurak yumshaydi.",
    "O‘lim eshikni taqillatib kirmaydi. Shuning uchun tayyorgarlik bugun boshlanadi.",
    "Tavba qilishdan uyalma. Uyalish kerak bo‘lgani gunoh edi, qaytish emas.",
    "Boshqani kechirgan qalb, o‘zining kechirilishiga yaqinlashadi.",
    "Kimga ko‘p ne’mat berilgan bo‘lsa, undan ko‘p narsa so‘raladi. Ne’matlaringning savoli oldinda.",
    "Bugun ham yuragingning urishi — yana bir imkoniyat. Uni bekorga o‘tkazma.",
    "Safaring uzoq. Yo‘l ozig‘ing qanchalik? Eng yaxshi ozuqa taqvodir.",
    "Pul bilan ko‘p narsani sotib olasan, lekin umrning bir daqiqasini ham qaytarib ola olmaysan.",
    "Onang senga duo qilgan bo‘lsa, bu eng katta boylikdir. Unga bugun qo‘ng‘iroq qil.",
    "Hamma seni maqtasa-yu, Alloh oldida ahvoling yomon bo‘lsa, bu maqtovdan nima foyda?",
    "Yolg‘izlikda Allohdan qo‘rqish haqiqiy imonning belgisi. Hech kim ko‘rmayotganda sen kimsan?",
    "Pushaymon bo‘lib “kashki” deyishdan oldin, bugun “ey Rabbim” deb qayt.",
    "Jannat arzon emas, ammo qiyin ham emas: namoz, taqvo, sabr. Yo‘l shu.",
    "Bugun bir kishining dilini xursand qilsang, o‘sha yaxshilik izsiz ketmaydi.",
    "Eshik ochiq, lekin umr eshigi yopilishi mumkin. Qaytishni kechiktirma.",
    "Hayot — imtihon. Imtihonda o‘zingni qanday tutayotganingga e’tibor ber.",
    "Qalbni ham kiyim kabi yuvish kerak: istig‘for bilan.",
    "Gunohning kichikligiga emas, kimga qarshi qilinayotganiga qara.",
    "Dunyo — o‘tib ketiladigan ko‘prik. Ko‘prik ustiga uy qurma.",
    "Bugun nima qoldiryapsan: kimdir seni eslab duo qilishi uchun?",
    "Bugun uyqudan turding, kimdir turmadi. Bu — yana bir kun, qadrla.",
)]

AKHIRAH = _HADITH + _AYAT + _WORDS
random.Random(2026).shuffle(AKHIRAH)   # tartib har safar bir xil (restartda ham o'zgarmaydi)

# ------------------------------------------------------------------ ZIKR ESLATMALARI (faqat eslatadi)
# Zikrning o'zi Mini App'da o'qiladi. Bu yerda faqat zikrga undovchi hadis va oyatlar.
REMIND = [
    H("Rabbini zikr qilgan kishi bilan zikr qilmagan kishining o‘xshashi tirik va o‘lik kabidir.", "Buxoriy 6407"),
    H("Alloh Taolo aytadi: “Kim Meni ichida eslasa, Men ham uni ichimda eslayman. Kim Meni jamoada eslasa, Men uni undan yaxshiroq jamoada eslayman.”", "Buxoriy 7405, Muslim 2675"),
    H("Har tong otganda sizlardan har birining har bo‘g‘imi uchun sadaqa bor: har tasbeh sadaqa, har hamd sadaqa, har tahlil sadaqa, har takbir sadaqadir.", "Muslim 720"),
    H("Kim kuniga yuz marta “Subhanallohi va bihamdihi” desa, gunohlari dengiz ko‘pigicha bo‘lsa ham kechiriladi.", "Buxoriy 6405, Muslim 2691"),
    H("Sizlardan biringiz kuniga mingta savob qozonishdan ojizmi? Yuz marta tasbeh aytsa, o‘zi uchun ming savob yoziladi yoki ming xato o‘chiriladi.", "Muslim 2698"),
    H("Ikki kalima tilga yengil, mezonda og‘ir, Rahmonga suyukli: “Subhanallohi va bihamdihi, Subhanallohil Azim”.", "Buxoriy 6406, Muslim 2694"),
    H("“Subhanalloh, Alhamdulillah, La ilaha illalloh, Allohu akbar” deyishim menga quyosh nur sochgan hamma narsadan suyukliroqdir.", "Muslim 2695"),
    H("“La havla va la quvvata illa billah” jannat xazinalaridan bir xazinadir.", "Buxoriy 6384, Muslim 2704"),
    H("Kim menga bir marta salovat aytsa, Alloh unga o‘n marta salovat aytadi.", "Muslim 408"),
    H("Ey odamlar, Allohga tavba qilinglar! Men kuniga yuz marta Unga tavba qilaman.", "Muslim 2702"),
    H("Kim sayyidul istig‘forni ishonch bilan aytsa va o‘sha kun (yoki kecha) vafot etsa, jannat ahlidan bo‘ladi.", "Buxoriy 6306"),
    H("Alloh Taolo aytadi: “Men bandam Menga qanday gumon qilsa, shundayman. U Meni eslaganda, Men u bilanman.”", "Buxoriy 7405, Muslim 2675"),
    H("Kim kuniga yuz marta “La ilaha illallohu vahdahu la sharika lah...” desa, o‘nta qul ozod qilgan savobini oladi va kun bo‘yi shaytondan himoyada bo‘ladi.", "Buxoriy 3293, Muslim 2691"),
] + [Q(r) for r in ("2:152", "13:28", "33:41", "7:205", "20:130", "50:39", "40:55", "76:25", "33:42", "62:10", "8:45", "29:45")]
random.Random(7).shuffle(REMIND)
