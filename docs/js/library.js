/* TAQVO PRO MAX — Duolar, Sahih hadis, Allohning 99 ismi.
   Hadislar faqat Buxoriy va Muslimdan (ma'nosi o'zbekchada; arabcha matn tasdiqlangan manbasiz kiritilmadi).
   Qur'on duolarining matni va tarjimasi alquran.cloud API'dan. Raqamlarni nashrdan oldin sunnah.com'da tekshiring. */
(() => {
  const el = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; };
  const get = async (ref) => {
    const k = 'qa:' + ref; try { const c = localStorage.getItem(k); if (c) return JSON.parse(c); } catch (e) {}
    const r = await fetch('https://api.alquran.cloud/v1/ayah/' + ref + '/editions/quran-uthmani,uz.sodik');
    if (!r.ok) throw new Error(r.status); const d = (await r.json()).data; const o = { ar: d[0].text, uz: d[1].text };
    try { localStorage.setItem(k, JSON.stringify(o)); } catch (e) {} return o;
  };
  const chips = (root, cats, cur, on) => { const b = el('div', 'q-tabs'); cats.forEach((c) => { const x = el('button', 'zk-chip' + (c === cur ? ' act' : ''), c); x.onclick = () => on(c); b.appendChild(x); }); root.appendChild(b); };
  const card = (title, ar, uz, src) => { const c = el('div', 'zk-card'); c.style.marginBottom = '10px';
    if (title) c.appendChild(el('h3', null, title));
    if (ar != null) { const a = el('p', 'zk-ar', ar); a.dir = 'rtl'; a.lang = 'ar'; c.appendChild(a); }
    const u = el('p', 'zk-uz', uz); c.appendChild(u); c.appendChild(el('p', 'zk-src', 'Manba: ' + src)); return { c, a: c.querySelector('.zk-ar'), u }; };

  // ---------------- DUOLAR
  const DUAS = [
    ['Ovqat', 'Ovqat oldidan', 'بِسْمِ اللَّهِ', 'Alloh nomi bilan. O‘ng qo‘l bilan va o‘z oldingdan yeyish ham sunnat.', 'Buxoriy 5376, Muslim 2022'],
    ['Ovqat', 'Ovqatdan keyin', 'الْحَمْدُ لِلَّهِ الَّذِي أَطْعَمَنِي هَذَا وَرَزَقَنِيهِ مِنْ غَيْرِ حَوْلٍ مِنِّي وَلَا قُوَّةٍ', 'Meni shu bilan oziqlantirgan va menga uni o‘z kuchim va qudratimsiz rizq qilib bergan Allohga hamd bo‘lsin.', 'Abu Dovud 4023, Termiziy 3458'],
    ['Uyqu', 'Uyquga yotganda', 'بِاسْمِكَ اللَّهُمَّ أَمُوتُ وَأَحْيَا', 'Ey Allohim, Sening isming bilan o‘laman va yashayman.', 'Buxoriy 6324'],
    ['Uyqu', 'Uyg‘onganda', 'الْحَمْدُ لِلَّهِ الَّذِي أَحْيَانَا بَعْدَ مَا أَمَاتَنَا وَإِلَيْهِ النُّشُورُ', 'Bizni o‘ldirgandan keyin tiriltirgan Allohga hamd bo‘lsin. Qaytish Uning huzuriga.', 'Buxoriy 6324'],
    ['Safar', 'Hayvon yoki transportga minganda', 'سُبْحَانَ الَّذِي سَخَّرَ لَنَا هَذَا وَمَا كُنَّا لَهُ مُقْرِنِينَ وَإِنَّا إِلَى رَبِّنَا لَمُنْقَلِبُونَ', 'Buni bizga bo‘ysundirgan Zot pokdir, biz uni o‘zimiz bo‘ysundira olmas edik. Albatta, biz Rabbimizga qaytuvchimiz.', 'Qur’on 43:13-14, Muslim 1342'],
    ['Himoya', 'Uydan chiqayotganda', 'بِسْمِ اللَّهِ تَوَكَّلْتُ عَلَى اللَّهِ وَلَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ', 'Alloh nomi bilan, Allohga tavakkul qildim. Kuch va qudrat faqat Allohdadir.', 'Abu Dovud 5095, Termiziy 3426'],
    ['Himoya', 'Qiyinchilik va qo‘rquvda', 'حَسْبُنَا اللَّهُ وَنِعْمَ الْوَكِيلُ', 'Bizga Alloh kifoya, U qanday yaxshi vakildir.', 'Qur’on 3:173, Buxoriy 4563'],
    ['Himoya', 'Hojatxonaga kirganda', 'اللَّهُمَّ إِنِّي أَعُوذُ بِكَ مِنَ الْخُبُثِ وَالْخَبَائِثِ', 'Ey Allohim, erkak va urg‘ochi shaytonlardan Senga panoh tilayman.', 'Buxoriy 142, Muslim 375'],
    ['Kundalik', 'Dunyo va oxirat yaxshiligi', null, '', 'Qur’on 2:201; Anas roziyallohu anhu: Payg‘ambar ﷺ eng ko‘p shu duoni qilardilar (Buxoriy 6389)', '2:201'],
    ['Kundalik', 'Ilm ziyoda bo‘lishi uchun', null, '', 'Qur’on 20:114', '20:114'],
    ['Mag‘firat', 'Odam Ato va Momo Havo duosi', null, '', 'Qur’on 7:23', '7:23'],
    ['Mag‘firat', 'Yunus alayhissalom duosi', null, '', 'Qur’on 21:87', '21:87'],
    ['Oila', 'Oila va farzandlar uchun', null, '', 'Qur’on 25:74', '25:74'],
    ['Oila', 'Ibrohim alayhissalom duosi', null, '', 'Qur’on 14:40', '14:40'],
  ];
  function duas(root, cat) {
    root.textContent = ''; cat = cat || 'Hammasi';
    chips(root, ['Hammasi', ...new Set(DUAS.map((d) => d[0]))], cat, (c) => duas(root, c));
    DUAS.filter((d) => cat === 'Hammasi' || d[0] === cat).forEach((d) => {
      const x = card(d[1], d[2], d[3], d[4]); root.appendChild(x.c);
      if (d[5]) { x.a.textContent = 'Yuklanmoqda…'; get(d[5]).then((v) => { x.a.textContent = v.ar; x.u.textContent = v.uz; }).catch(() => { x.a.textContent = ''; x.u.textContent = 'Matnni yuklab bo‘lmadi. Internetni tekshiring.'; }); }
    });
    root.appendChild(el('p', 'zk-src', 'Tonggi va kechki duolar “Zikr” bo‘limlarida. Hadisdagi duolarning o‘qilishi (transliteratsiya) keyingi yangilanishda qo‘shiladi.'));
    return { title: 'Duolar', status: DUAS.length + ' ta dua' };
  }

  // ---------------- SAHIH HADIS
  const HADITH = [
    ['Niyat', 'Amallar niyatlarga bog‘liqdir. Har kishiga faqat niyat qilgani bor.', 'Buxoriy 1, Muslim 1907'],
    ['Axloq', 'Sizlardan biringiz o‘zi uchun yoqtirganni birodari uchun ham yoqtirmaguncha iymon keltirmagan bo‘ladi.', 'Buxoriy 13, Muslim 45'],
    ['Axloq', 'Kim Allohga va oxirat kuniga iymon keltirgan bo‘lsa, yaxshi gapirsin yoki sukut qilsin.', 'Buxoriy 6018, Muslim 47'],
    ['Axloq', 'Kuchli polvon kurashda yengadigan emas. Haqiqiy kuchli — g‘azab paytida o‘zini tuta oladigan kishidir.', 'Buxoriy 6114, Muslim 2609'],
    ['Axloq', 'Mo‘min mo‘minga bir-birini mustahkamlab turuvchi bino kabidir.', 'Buxoriy 481, Muslim 2585'],
    ['Axloq', 'Kim bir mo‘minning dunyo tashvishlaridan birini ketkazsa, Alloh uning qiyomat kuni tashvishlaridan birini ketkazadi.', 'Muslim 2699'],
    ['Sadaqa', 'Yarim xurmo bilan bo‘lsa ham o‘zingizni do‘zaxdan saqlang.', 'Buxoriy 1417, Muslim 1016'],
    ['Sadaqa', 'Inson vafot etsa, amali uziladi, faqat uch narsa qoladi: sadaqai joriya, foydali ilm yoki unga duo qiladigan solih farzand.', 'Muslim 1631'],
    ['Oxirat', 'Dunyoda go‘yo g‘arib yoki yo‘lovchidek bo‘l.', 'Buxoriy 6416'],
    ['Oxirat', 'Ikki ne’mat borki, ko‘p odamlar ularda aldanib qoladi: sog‘lik va bo‘sh vaqt.', 'Buxoriy 6412'],
    ['Oxirat', 'Kim Allohning huzuriga yo‘liqishni yoqtirsa, Alloh ham uning huzuriga yo‘liqishni yoqtiradi.', 'Buxoriy 6507, Muslim 2683'],
    ['Zikr', 'Ikki kalima tilga yengil, mezonda og‘ir, Rahmonga suyukli: “Subhanallohi va bihamdihi, Subhanallohil Azim”.', 'Buxoriy 6406, Muslim 2694'],
    ['Zikr', 'Rabbini zikr qilgan kishi bilan zikr qilmagan kishining o‘xshashi tirik va o‘lik kabidir.', 'Buxoriy 6407'],
    ['Tavba', 'Ey odamlar, Allohga tavba qilinglar! Men kuniga yuz marta Unga tavba qilaman.', 'Muslim 2702'],
  ];
  function hadith(root, cat) {
    root.textContent = ''; cat = cat || 'Hammasi';
    chips(root, ['Hammasi', ...new Set(HADITH.map((h) => h[0]))], cat, (c) => hadith(root, c));
    HADITH.filter((h) => cat === 'Hammasi' || h[0] === cat).forEach((h) => root.appendChild(card(h[0], null, h[1], h[2]).c));
    root.appendChild(el('p', 'zk-src', 'Faqat Buxoriy va Muslim (Sahihayn). Matnlar o‘zbekcha ma’nosi. Arabcha matn va ko‘proq hadis keyingi yangilanishda tasdiqlangan manbadan qo‘shiladi.'));
    return { title: 'Sahih hadis', status: HADITH.length + ' ta hadis' };
  }

  // ---------------- 99 ISM
  const N = `الله|Alloh|Yagona ma’bud
الرحمن|Ar-Rohman|Behad mehribon
الرحيم|Ar-Rohiym|Rahmi cheksiz
الملك|Al-Malik|Podshoh
القدوس|Al-Quddus|Eng pok
السلام|As-Salom|Omonlik beruvchi
المؤمن|Al-Mu’min|Omonlik va iymon beruvchi
المهيمن|Al-Muhaymin|Hamma narsani kuzatuvchi
العزيز|Al-Aziz|Qudratli
الجبار|Al-Jabbor|Hukmi o‘tkir
المتكبر|Al-Mutakabbir|Buyuklikda yagona
الخالق|Al-Xoliq|Yaratuvchi
البارئ|Al-Bori’|Yo‘qdan bor qiluvchi
المصور|Al-Musavvir|Shakl beruvchi
الغفار|Al-G‘offar|Ko‘p mag‘firat qiluvchi
القهار|Al-Qohhor|Hammani bo‘ysundiruvchi
الوهاب|Al-Vahhob|Ko‘p in’om etuvchi
الرزاق|Ar-Rozzoq|Rizq beruvchi
الفتاح|Al-Fattoh|Eshiklarni ochuvchi
العليم|Al-‘Aliym|Hamma narsani biluvchi
القابض|Al-Qobid|Rizqni toraytiruvchi
الباسط|Al-Bosit|Rizqni kengaytiruvchi
الخافض|Al-Xofid|Pasaytiruvchi
الرافع|Ar-Rofi’|Ko‘taruvchi
المعز|Al-Mu’izz|Izzat beruvchi
المذل|Al-Muzill|Xor qiluvchi
السميع|As-Sami’|Eshituvchi
البصير|Al-Basir|Ko‘ruvchi
الحكم|Al-Hakam|Hukm qiluvchi
العدل|Al-‘Adl|Adolatli
اللطيف|Al-Latif|Lutf qiluvchi
الخبير|Al-Xobir|Hamma narsadan xabardor
الحليم|Al-Halim|Sabrli, yumshoq
العظيم|Al-‘Azim|Ulug‘
الغفور|Al-G‘ofur|Mag‘firati ko‘p
الشكور|Ash-Shakur|Qadrlovchi
العلي|Al-‘Aliy|Oliy
الكبير|Al-Kabir|Buyuk
الحفيظ|Al-Hafiz|Saqlovchi
المقيت|Al-Muqit|Rizq va kuch beruvchi
الحسيب|Al-Hasib|Hisob oluvchi
الجليل|Al-Jalil|Ulug‘ sifatli
الكريم|Al-Karim|Karamli
الرقيب|Ar-Roqib|Kuzatib turuvchi
المجيب|Al-Mujib|Duoni ijobat qiluvchi
الواسع|Al-Vasi’|Qamrovi keng
الحكيم|Al-Hakim|Hikmatli
الودود|Al-Vadud|Sevuvchi
المجيد|Al-Majid|Shonli
الباعث|Al-Bo’is|Tiriltiruvchi
الشهيد|Ash-Shahid|Hamma narsaga guvoh
الحق|Al-Haqq|Haq
الوكيل|Al-Vakil|Ishonchli vakil
القوي|Al-Qaviy|Kuchli
المتين|Al-Matin|Mustahkam
الولي|Al-Valiy|Do‘st va yordamchi
الحميد|Al-Hamid|Maqtovga loyiq
المحصي|Al-Muhsi|Hamma narsani sanovchi
المبدئ|Al-Mubdi’|Boshlovchi
المعيد|Al-Mu’id|Qaytaruvchi
المحيي|Al-Muhyi|Hayot beruvchi
المميت|Al-Mumit|O‘ldiruvchi
الحي|Al-Hayy|Tirik
القيوم|Al-Qayyum|Qoim turuvchi
الواجد|Al-Vajid|Hamma narsani topuvchi
الماجد|Al-Maajid|Ulug‘vor
الواحد|Al-Vahid|Bir
الأحد|Al-Ahad|Yagona
الصمد|As-Somad|Hech narsaga muhtoj emas
القادر|Al-Qodir|Qodir
المقتدر|Al-Muqtadir|Qudrati cheksiz
المقدم|Al-Muqaddim|Oldinga suruvchi
المؤخر|Al-Mu’axxir|Orqaga suruvchi
الأول|Al-Avval|Birinchi
الآخر|Al-Aaxir|Oxirgi
الظاهر|Az-Zohir|Zohir
الباطن|Al-Botin|Botin
الوالي|Al-Voliy|Boshqaruvchi
المتعالي|Al-Muta’oliy|Oliy darajali
البر|Al-Barr|Yaxshilik qiluvchi
التواب|At-Tavvob|Tavbani qabul qiluvchi
المنتقم|Al-Muntaqim|Jazolovchi
العفو|Al-‘Afuvv|Afv etuvchi
الرؤوف|Ar-Ro’uf|Shafqatli
مالك الملك|Molikul-Mulk|Mulk egasi
ذو الجلال والإكرام|Zul-Jalol val-Ikrom|Ulug‘lik va karam egasi
المقسط|Al-Muqsit|Adolat qiluvchi
الجامع|Al-Jomi’|Jamlovchi
الغني|Al-G‘oniy|Behojat
المغني|Al-Mug‘niy|Boy qiluvchi
المانع|Al-Mani’|To‘suvchi
الضار|Ad-Dorr|Zarar yetkazuvchi
النافع|An-Nafi’|Foyda beruvchi
النور|An-Nur|Nur
الهادي|Al-Hadiy|Hidoyat qiluvchi
البديع|Al-Badi’|Misoli yo‘q yaratuvchi
الباقي|Al-Boqiy|Boqiy
الوارث|Al-Voris|Merosxo‘r
الرشيد|Ar-Rashid|To‘g‘ri yo‘lga boshlovchi`.split('\n').map((l) => l.split('|'));
  function names(root) {
    root.textContent = '';
    root.appendChild(el('p', 'zk-note', 'Allohning to‘qson to‘qqizta ismi bor. Kim ularni (ma’nosini bilib, amal qilib) sanasa, jannatga kiradi. (Buxoriy 2736, Muslim 2677)'));
    const q = el('input', 'q-search'); q.type = 'search'; q.placeholder = 'Ism qidirish'; root.appendChild(q);
    const box = el('div'); root.appendChild(box);
    const draw = () => { const t = q.value.trim().toLowerCase(); box.textContent = '';
      N.forEach((n, i) => { if (t && !(n[1] + n[2] + n[0] + (i + 1)).toLowerCase().includes(t)) return;
        const r = el('div', 'zk-row'); const l = el('div'); l.appendChild(el('b', null, (i + 1) + '. ' + n[1])); l.appendChild(el('p', 'zk-src', n[2]));
        r.appendChild(l); r.appendChild(el('span', 'q-arn', n[0])); box.appendChild(r); }); };
    q.oninput = draw; draw();
    root.appendChild(el('p', 'zk-src', 'Sahih hadisda ismlar soni aytilgan, aniq ro‘yxati esa keltirilmagan. Bu keng tarqalgan an’anaviy ro‘yxat; ulamolar o‘rtasida ayrim ismlarda farq bor.'));
    return { title: 'Allohning 99 ismi', status: '99 ta ism' };
  }

  window.TaqvoSections = window.TaqvoSections || {};
  Object.assign(window.TaqvoSections, { duas, hadith, names });
})();
