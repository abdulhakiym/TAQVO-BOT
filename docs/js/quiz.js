/* TAQVO PRO MAX - quiz.js (viktorina va shaxsiy reyting) */
(function () {
  'use strict';
  var T = window.TAQVO;

  var CATS = [
    { id: 'quran', t: 'Qur’on', i: '📖' },
    { id: 'hadith', t: 'Hadis', i: '📜' },
    { id: 'siyrat', t: 'Siyrat', i: '🌙' },
    { id: 'sahoba', t: 'Sahobalar', i: '🛡️' },
    { id: 'tarix', t: 'Islom tarixi', i: '🏛️' },
    { id: 'fiqh', t: 'Fiqh asoslari', i: '⚖️' }
  ];
  var LEVELS = [
    { n: 'Yangi talaba', x: 0 }, { n: 'Talaba', x: 100 }, { n: 'Bilimdon', x: 300 },
    { n: 'Mohir', x: 600 }, { n: 'Dono', x: 1000 }
  ];
  var XP_OK = 10, XP_DAILY = 20;

  // Har bir savolda o[0] to'g'ri javob; ko'rsatishdan oldin aralashtiriladi.
  var Q = [
    // ---- Qur'on ----
    { c: 'quran', q: 'Qur’oni Karimda nechta sura bor?', o: ['114', '110', '120', '124'], e: 'Qur’on 114 sura va 30 poradan iborat.' },
    { c: 'quran', q: 'Qur’onning eng uzun surasi qaysi?', o: ['Baqara', 'Oli Imron', 'Niso', 'Moida'], e: 'Baqara surasi 286 oyatdan iborat.' },
    { c: 'quran', q: 'Fotiha surasi necha oyatdan iborat?', o: ['7', '5', '9', '10'], e: 'Fotiha 7 oyatdan iborat va Qur’onning ochuvchi surasidir.' },
    { c: 'quran', q: 'Qaysi surada boshida «Bismillah» yozilmagan?', o: ['Tavba', 'Yosin', 'Kahf', 'Muzzammil'], e: 'Tavba (Bara’a) surasi Bismillahsiz boshlanadi.' },
    { c: 'quran', q: 'Qur’on qaysi kechada nozil qilina boshlagan?', o: ['Qadr kechasi', 'Arafa kechasi', 'Juma kechasi', 'Hijrat kechasi'], e: 'Qadr surasi 1-oyatda Qur’on Qadr kechasida nozil qilingani aytilgan. Ramazon oyi ekani Baqara surasi 185-oyatda kelgan.' },
    { c: 'quran', q: 'Qur’onda ismlari zikr qilingan payg‘ambarlar soni nechta?', o: ['25', '20', '30', '40'], e: 'Qur’onda 25 payg‘ambarning ismi zikr qilingan.' },
    { c: 'quran', q: 'Hadisda «Allohning kitobidagi eng ulug‘ oyat» deb aytilgan oyat qaysi?', o: ['Oyatul Kursiy', 'Ixlos surasi', 'Fotihaning 1-oyati', 'Omanarrasulu'], e: 'Sahih Muslim 810: Ubay ibn Ka’b (r.a.) ga shunday javob berilgan.' },
    { c: 'quran', q: 'Qur’onning eng qisqa surasi (so‘zlar soni jihatidan) qaysi?', o: ['Kavsar', 'Ixlos', 'Falaq', 'Nos'], e: 'Kavsar surasi 3 oyatdan iborat va so‘zlari eng kam.' },
    // ---- Hadis ----
    { c: 'hadith', q: 'Sahih al-Buxoriy kitobining muallifi kim?', o: ['Imom Buxoriy', 'Imom Muslim', 'Imom Termiziy', 'Imom Molik'], e: 'Muhammad ibn Ismoil al-Buxoriy (rahimahulloh) Buxoroda tug‘ilgan.' },
    { c: 'hadith', q: '«Sahihayn» deganda qaysi ikki to‘plam nazarda tutiladi?', o: ['Buxoriy va Muslim', 'Buxoriy va Termiziy', 'Muslim va Abu Dovud', 'Nasoiy va Ibn Moja'], e: 'Sahihayn: Sahih al-Buxoriy va Sahih Muslim.' },
    { c: 'hadith', q: 'Sahih al-Buxoriydagi birinchi hadis qaysi mavzuda?', o: ['Niyat', 'Namoz', 'Zakot', 'Haj'], e: '«Amallar niyatlarga bog‘liqdir» hadisi kitobning 1-hadisi (Sahih Muslim 1907 da ham bor).' },
    { c: 'hadith', q: '«Al-Muvatta» kitobining muallifi kim?', o: ['Imom Molik', 'Imom Shofiiy', 'Imom Ahmad', 'Imom Abu Hanifa'], e: 'Al-Muvatta Imom Molik ibn Anasning asaridir.' },
    { c: 'hadith', q: '«Musnad» nomli mashhur hadis to‘plami muallifi kim?', o: ['Imom Ahmad ibn Hanbal', 'Imom Nasoiy', 'Imom Ibn Moja', 'Imom Abu Dovud'], e: 'Musnad Ahmad — Imom Ahmad ibn Hanbalning katta to‘plami.' },
    { c: 'hadith', q: 'Hadis darajalaridan eng yuqorisi qaysi?', o: ['Sahih', 'Hasan', 'Zaif', 'Mavzu‘ (to‘qima)'], e: 'Sahih hadis: ravilari odil va zobit, sanadi uzilmagan, shoz va illatdan xoli.' },
    { c: 'hadith', q: 'Imom Navaviyning «Arba’in» to‘plamida nechta hadis bor?', o: ['42', '40', '30', '50'], e: 'Nomi «qirq» bo‘lsa ham, mashhur nusxasida 42 ta hadis bor.' },
    { c: 'hadith', q: 'Sahih Muslim kitobi muallifi kim?', o: ['Imom Muslim ibn al-Hajjoj', 'Imom Buxoriy', 'Imom Termiziy', 'Imom Nasoiy'], e: 'Sahih Muslim Imom Muslim ibn al-Hajjoj an-Naysaburiyning asaridir.' },
    // ---- Siyrat ----
    { c: 'siyrat', q: 'Payg‘ambarimiz ﷺ qaysi shaharda tug‘ilgan?', o: ['Makka', 'Madina', 'Toif', 'Quddus'], e: 'Payg‘ambarimiz ﷺ Makkai Mukarramada, Fil yilida tug‘ilgan (ko‘pchilik ulamolar fikri).' },
    { c: 'siyrat', q: 'Payg‘ambarimiz ﷺ ning otalarining ismi nima?', o: ['Abdulloh', 'Abu Tolib', 'Abdulmuttalib', 'Abu Lahab'], e: 'Otalari Abdulloh, onalari Omina binti Vahb.' },
    { c: 'siyrat', q: 'Birinchi vahiy qayerda kelgan?', o: ['Hiro g‘ori', 'Savr g‘ori', 'Uhud tog‘i', 'Arafot'], e: 'Makka yaqinidagi Nur tog‘ida joylashgan Hiro g‘origa Jabroil (a.s.) kelgan (Sahih al-Buxoriy 3).' },
    { c: 'siyrat', q: 'Birinchi nozil bo‘lgan oyatlar qaysi suradan?', o: ['Alaq', 'Muddassir', 'Fotiha', 'Muzzammil'], e: 'Ko‘pchilik ulamolarga ko‘ra, dastlab Alaq surasining «Iqra» oyatlari nozil bo‘lgan.' },
    { c: 'siyrat', q: 'Payg‘ambarimiz ﷺ ning birinchi turmush o‘rtog‘i kim?', o: ['Xadija binti Xuvaylid', 'Oisha binti Abu Bakr', 'Hafsa binti Umar', 'Zaynab binti Jahsh'], e: 'Xadija (r.a.) bilan nikoh Payg‘ambarlikdan oldin bo‘lgan.' },
    { c: 'siyrat', q: 'Payg‘ambarimiz ﷺ Makkadan qaysi shaharga hijrat qildilar?', o: ['Madina', 'Toif', 'Quddus', 'Damashq'], e: 'Madina (avval Yasrib deb atalgan) shahriga hijrat qildilar.' },
    { c: 'siyrat', q: 'Hijrat safarida g‘orda Payg‘ambar ﷺ bilan birga bo‘lgan sahoba kim?', o: ['Abu Bakr as-Siddiq', 'Umar ibn Xattob', 'Ali ibn Abu Tolib', 'Usmon ibn Affon'], e: 'Savr g‘orida bo‘lgan; Tavba surasi 40-oyatda «ikkitaning ikkinchisi» deb zikr etilgan.' },
    { c: 'siyrat', q: 'Hijratdan keyin qurilgan birinchi masjid qaysi?', o: ['Quba masjidi', 'Masjidul Aqso', 'Masjidul Haram', 'Masjidi Nabaviy'], e: 'Madinaga kirishdan oldin Quba qishlog‘ida qurilgan.' },
    { c: 'siyrat', q: 'Badr jangi hijriy qaysi yilda bo‘lgan?', o: ['2-yil', '1-yil', '3-yil', '5-yil'], e: 'Badr jangi hijriy 2-yil Ramazon oyida bo‘lgan.' },
    { c: 'siyrat', q: 'Uhud jangi hijriy qaysi yilda bo‘lgan?', o: ['3-yil', '2-yil', '5-yil', '8-yil'], e: 'Uhud jangi hijriy 3-yil Shavvol oyida bo‘lgan.' },
    { c: 'siyrat', q: 'Makka fathi hijriy qaysi yilda bo‘lgan?', o: ['8-yil', '6-yil', '10-yil', '5-yil'], e: 'Makka fathi hijriy 8-yil Ramazon oyida sodir bo‘lgan.' },
    { c: 'siyrat', q: 'Vido hajji hijriy qaysi yilda bo‘lgan?', o: ['10-yil', '8-yil', '9-yil', '11-yil'], e: 'Hijriy 10-yilda; Arafotdagi xutba «Vido xutbasi» deb ataladi.' },
    { c: 'siyrat', q: 'Payg‘ambarimiz ﷺ necha yoshda vafot etganlar?', o: ['63', '60', '70', '65'], e: 'Sahih Muslim: Oisha (r.a.) rivoyatiga ko‘ra, 63 yoshda vafot etganlar.' },
    // ---- Sahobalar ----
    { c: 'sahoba', q: 'Qaysi sahoba «Siddiq» laqabi bilan mashhur?', o: ['Abu Bakr', 'Umar', 'Usmon', 'Ali'], e: 'Abu Bakr as-Siddiq (r.a.) Payg‘ambar ﷺ ni doimo tasdiqlagani uchun shunday laqab olgan.' },
    { c: 'sahoba', q: 'Qaysi sahoba «Foruq» laqabi bilan mashhur?', o: ['Umar ibn Xattob', 'Abu Bakr', 'Usmon', 'Xolid ibn Valid'], e: 'Umar ibn Xattob (r.a.) haq bilan botilni ajratgani uchun «Foruq» deyilgan.' },
    { c: 'sahoba', q: '«Zun-Nurayn» (ikki nur egasi) laqabi qaysi sahobaga berilgan?', o: ['Usmon ibn Affon', 'Ali ibn Abu Tolib', 'Zubayr ibn Avvom', 'Talha ibn Ubaydulloh'], e: 'Payg‘ambar ﷺ ning ikki qiziga ketma-ket uylangani uchun.' },
    { c: 'sahoba', q: '«Sayfulloh» (Allohning qilichi) laqabi kimga berilgan?', o: ['Xolid ibn Valid', 'Hamza ibn Abdulmuttalib', 'Sa’d ibn Abu Vaqqos', 'Zayd ibn Harisa'], e: 'Xolid ibn Valid (r.a.) ga Payg‘ambar ﷺ shu laqabni bergan.' },
    { c: 'sahoba', q: 'Islomdagi birinchi muazzin kim?', o: ['Bilol ibn Rabah', 'Ammor ibn Yosir', 'Salmon Forsiy', 'Anas ibn Malik'], e: 'Bilol ibn Rabah al-Habashiy (r.a.).' },
    { c: 'sahoba', q: 'Eng ko‘p hadis rivoyat qilgan sahoba kim?', o: ['Abu Hurayra', 'Oisha', 'Abdulloh ibn Umar', 'Anas ibn Malik'], e: 'Abu Hurayra (r.a.) eng ko‘p hadis rivoyat qilgan sahobadir.' },
    { c: 'sahoba', q: 'Hijratdan oldin Madinaga Islomni o‘rgatish uchun yuborilgan sahoba kim?', o: ['Mus’ab ibn Umayr', 'Bilol ibn Rabah', 'Abu Ubayda', 'Zayd ibn Sobit'], e: 'Mus’ab ibn Umayr (r.a.). Keyinchalik Uhud jangida bayroqdor bo‘lib shahid bo‘lgan.' },
    { c: 'sahoba', q: 'Xandaq jangida Madina atrofiga xandaq qazishni kim maslahat bergan?', o: ['Salmon Forsiy', 'Abu Bakr', 'Umar ibn Xattob', 'Ali ibn Abu Tolib'], e: 'Bu fikrni Salmon al-Forsiy (r.a.) bildirgan.' },
    // ---- Islom tarixi ----
    { c: 'tarix', q: 'Payg‘ambar ﷺ dan keyingi birinchi xalifa kim?', o: ['Abu Bakr', 'Umar', 'Usmon', 'Ali'], e: 'Xulafoi roshidinning tartibi: Abu Bakr, Umar, Usmon, Ali (r.a.).' },
    { c: 'tarix', q: 'To‘rt xalifadan eng oxirgisi kim?', o: ['Ali ibn Abu Tolib', 'Usmon ibn Affon', 'Umar ibn Xattob', 'Abu Bakr'], e: 'Ali ibn Abu Tolib (r.a.) to‘rtinchi xalifa.' },
    { c: 'tarix', q: 'Hijriy yil hisobi kimning xalifaligi davrida joriy etilgan?', o: ['Umar ibn Xattob', 'Abu Bakr', 'Usmon ibn Affon', 'Ali ibn Abu Tolib'], e: 'Hisob boshi sifatida Payg‘ambar ﷺ ning hijrati olingan.' },
    { c: 'tarix', q: 'Qur’on mushaf nusxalari ko‘paytirilib turli o‘lkalarga yuborilgan xalifa kim?', o: ['Usmon ibn Affon', 'Abu Bakr', 'Umar ibn Xattob', 'Ali ibn Abu Tolib'], e: 'Usmon (r.a.) davrida mushaf nusxalari yozdirilib, o‘lkalarga jo‘natilgan.' },
    { c: 'tarix', q: 'Umaviylar xalifaligining poytaxti qaysi shahar edi?', o: ['Damashq', 'Bag‘dod', 'Qohira', 'Makka'], e: 'Umaviylar poytaxti Damashq bo‘lgan.' },
    { c: 'tarix', q: 'Abbosiylar xalifaligining mashhur poytaxti qaysi shahar?', o: ['Bag‘dod', 'Damashq', 'Qohira', 'Madina'], e: 'Abbosiylar poytaxti Bag‘dod bo‘lgan.' },
    { c: 'tarix', q: 'Imom Buxoriy qaysi shaharda tug‘ilgan?', o: ['Buxoro', 'Samarqand', 'Termiz', 'Nishopur'], e: 'Imom Buxoriy Buxoroda, hijriy 194 (milodiy 810) yilda tug‘ilgan.' },
    { c: 'tarix', q: 'Salohiddin Ayyubiy Quddusni qaysi milodiy yilda qaytarib oldi?', o: ['1187', '1099', '1258', '1453'], e: 'Hattin jangidan keyin, 1187 yilda.' },
    // ---- Fiqh asoslari ----
    { c: 'fiqh', q: 'Islomning ruknlari nechta?', o: ['5', '4', '6', '7'], e: 'Shahodat, namoz, zakot, ro‘za va haj (Sahih al-Buxoriy va Muslim).' },
    { c: 'fiqh', q: 'Kun davomida nechta farz namoz o‘qiladi?', o: ['5', '3', '4', '6'], e: 'Bomdod, Peshin, Asr, Shom va Xufton.' },
    { c: 'fiqh', q: 'Shom namozining farzi necha rakat?', o: ['3', '2', '4', '5'], e: 'Shom namozi farzi 3 rakat.' },
    { c: 'fiqh', q: 'Ro‘za qaysi oyda tutiladi?', o: ['Ramazon', 'Shaʼbon', 'Muharram', 'Zulhijja'], e: 'Ramazon oyi ro‘zasi farz (Baqara, 183 va 185).' },
    { c: 'fiqh', q: 'Moida surasi 6-oyatida tahorat uchun qaysi a’zolar zikr qilingan?', o: ['Yuz, qo‘llar, boshni mash, oyoqlar', 'Faqat qo‘llar va oyoqlar', 'Yuz, quloq, bo‘yin, oyoqlar', 'Yuz, qo‘l va tizza'], e: 'Yuzni, qo‘llarni tirsaklargacha yuvish, boshni mash qilish va oyoqlarni to‘piqlargacha yuvish.' },
    { c: 'fiqh', q: 'Arafotda turish hajning qaysi kunida bo‘ladi?', o: ['9-Zulhijja', '8-Zulhijja', '10-Zulhijja', '1-Muharram'], e: 'Arafot kuni 9-Zulhijja; «Haj — Arafotdir» deb aytilgan.' },
    { c: 'fiqh', q: 'Hadisga ko‘ra, quyosh chiqqan kunlarning eng yaxshisi qaysi?', o: ['Juma', 'Dushanba', 'Payshanba', 'Yakshanba'], e: 'Sahih Muslim 854: quyosh chiqqan kunlarning eng yaxshisi juma kunidir.' }
  ];

  var el = null, Z = null, stats = null;

  /* ---------- YORDAMCHI ---------- */
  function esc(s) { return T.esc(s); }
  function hash(s) {
    var h = 2166136261;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function shuffle(arr, r) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(r() * (i + 1)), t = a[i];
      a[i] = a[j]; a[j] = t;
    }
    return a;
  }
  function today() {
    var d = new Date();
    return d.getFullYear() + '-' + T.pad(d.getMonth() + 1) + '-' + T.pad(d.getDate());
  }
  function catOf(id) {
    for (var i = 0; i < CATS.length; i++) if (CATS[i].id === id) return CATS[i];
    return { id: id, t: id, i: '❓' };
  }
  function count(cat) { return Q.filter(function (x) { return x.c === cat; }).length; }
  function levelOf(xp) {
    var idx = 0;
    for (var k = 0; k < LEVELS.length; k++) if (xp >= LEVELS[k].x) idx = k;
    return idx;
  }

  /* ---------- SAQLASH ---------- */
  function loadStats() {
    var s = T.store.get('quiz:stats', null) || {};
    return {
      xp: +s.xp || 0,
      cat: s.cat && typeof s.cat === 'object' ? s.cat : {},
      best: s.best && typeof s.best === 'object' ? s.best : {},
      daily: s.daily || null,
      hist: Array.isArray(s.hist) ? s.hist : []
    };
  }
  function saveStats() { T.store.set('quiz:stats', stats); }

  /* ---------- UMUMIY BLOKLAR ---------- */
  function levelHTML() {
    var i = levelOf(stats.xp), L = LEVELS[i], nx = LEVELS[i + 1];
    var pct = nx ? Math.round((stats.xp - L.x) / (nx.x - L.x) * 100) : 100;
    return '<div class="card glass"><div class="row between"><div><div class="muted small">Daraja</div>' +
      '<div style="font-size:20px;font-weight:700;color:var(--gold2)">' + esc(L.n) + '</div></div>' +
      '<div style="text-align:right"><div class="muted small">Ball</div><div style="font-size:20px;font-weight:700">' + stats.xp + '</div></div></div>' +
      '<div class="progress" style="margin-top:10px"><i style="width:' + pct + '%"></i></div>' +
      '<div class="src">' + (nx ? 'Keyingi daraja: ' + esc(nx.n) + ' (' + nx.x + ' ball)' : 'Eng yuqori darajaga yetdingiz') + '</div></div>';
  }

  /* ---------- MENYU ---------- */
  function showMenu() {
    Z = null;
    var h = levelHTML();
    var dd = stats.daily && stats.daily.date === today() ? stats.daily : null;
    h += '<div class="card"><div style="font-weight:700">🔥 Kunlik sinov</div>' +
      '<div class="muted small" style="margin:4px 0 10px">Har kuni 5 ta aralash savol. Bir kunda bir marta, bajarilsa +' + XP_DAILY + ' ball bonus.</div>';
    h += dd ? '<div class="chip sahih">Bugungi natija: ' + dd.s + ' / ' + dd.n + ' ✓</div><div class="src">Ertaga yangi sinov bo‘ladi.</div>'
            : '<button class="btn" data-a="start" data-c="daily">Boshlash</button>';
    h += '</div>';

    h += '<div class="muted small" style="margin-top:4px">Mavzuni tanlang (10 ta savol)</div>';
    CATS.forEach(function (c) {
      var b = stats.best[c.id];
      h += '<button class="list-item" data-a="start" data-c="' + c.id + '"><span class="num">' + c.i + '</span>' +
        '<span class="grow">' + esc(c.t) + '<div class="muted small">' + count(c.id) + ' ta savol' + (b != null ? ' · eng yaxshi: ' + b + '%' : '') + '</div></span>' +
        '<span class="muted">›</span></button>';
    });
    h += '<button class="btn" data-a="start" data-c="mix">🎲 Aralash (10 ta savol)</button>';
    h += '<div class="src">Savollar umumiy e’tirof etilgan ma’lumotlarga asoslangan. Bahsli masalalar ataylab kiritilmagan. Jami: ' + Q.length + ' ta savol.</div>';
    el.innerHTML = h;
    window.scrollTo(0, 0);
  }

  /* ---------- O'YIN ---------- */
  function startGame(cat) {
    var daily = cat === 'daily';
    var pool = Q.filter(function (x) { return daily || cat === 'mix' || x.c === cat; });
    var seed = daily ? hash('daily:' + today()) : Math.floor(Math.random() * 4294967296);
    var r = rng(seed);
    var n = Math.min(daily ? 5 : 10, pool.length);
    var qs = shuffle(pool, r).slice(0, n).map(function (x) {
      var opts = shuffle(x.o.map(function (t, i) { return { t: t, ok: i === 0 }; }), r);
      return { c: x.c, q: x.q, e: x.e, opts: opts };
    });
    Z = { cat: cat, daily: daily, qs: qs, i: 0, score: 0, ans: -1, log: [] };
    showQuestion();
  }

  function showQuestion() {
    var q = Z.qs[Z.i], n = Z.qs.length, answered = Z.ans >= 0;
    var cat = catOf(q.c);
    var h = '<div class="row between"><button class="btn ghost sm" data-a="menu">‹ Menyu</button>' +
      '<span class="chip">' + cat.i + ' ' + esc(cat.t) + '</span></div>';
    h += '<div class="card glass"><div class="row between small muted"><span>Savol ' + (Z.i + 1) + ' / ' + n + '</span><span>To‘g‘ri: ' + Z.score + '</span></div>' +
      '<div class="progress" style="margin:8px 0 12px"><i style="width:' + Math.round((Z.i + (answered ? 1 : 0)) / n * 100) + '%"></i></div>' +
      '<div style="font-size:18px;font-weight:600;line-height:1.45">' + esc(q.q) + '</div></div>';
    q.opts.forEach(function (o, k) {
      var st = '';
      if (answered) {
        if (o.ok) st = ' style="border-color:#8ee08e;background:rgba(76,175,80,.15)"';
        else if (k === Z.ans) st = ' style="border-color:#ff8a80;background:rgba(244,67,54,.15)"';
      }
      h += '<button class="list-item" data-a="ans" data-k="' + k + '"' + st + (answered ? ' disabled' : '') + '>' +
        '<span class="num">' + 'ABCD'.charAt(k) + '</span><span class="grow">' + esc(o.t) + '</span>' +
        (answered && o.ok ? '<span>✓</span>' : (answered && k === Z.ans ? '<span>✕</span>' : '')) + '</button>';
    });
    if (answered) {
      var ok = q.opts[Z.ans].ok;
      h += '<div class="card"><div style="font-weight:600;color:' + (ok ? '#8ee08e' : '#ff8a80') + '">' + (ok ? 'To‘g‘ri!' : 'Noto‘g‘ri') + '</div>' +
        '<div class="meaning">' + esc(q.e) + '</div></div>' +
        '<button class="btn" data-a="next">' + (Z.i + 1 < n ? 'Keyingi ›' : 'Natijani ko‘rish') + '</button>';
    }
    el.innerHTML = h;
  }

  function answer(k) {
    if (!Z || Z.ans >= 0) return;
    var q = Z.qs[Z.i];
    Z.ans = k;
    var ok = q.opts[k].ok;
    if (ok) Z.score++;
    Z.log.push({ c: q.c, ok: ok });
    T.tg.haptic(ok ? 'success' : 'error');
    showQuestion();
  }

  function finish() {
    var n = Z.qs.length, before = levelOf(stats.xp);
    var gained = Z.score * XP_OK + (Z.daily ? XP_DAILY : 0);
    stats.xp += gained;
    Z.log.forEach(function (x) {
      var c = stats.cat[x.c] || { t: 0, c: 0 };
      c.t++; if (x.ok) c.c++;
      stats.cat[x.c] = c;
    });
    var pct = Math.round(Z.score / n * 100);
    if (!Z.daily && (stats.best[Z.cat] == null || pct > stats.best[Z.cat])) stats.best[Z.cat] = pct;
    if (Z.daily) stats.daily = { date: today(), s: Z.score, n: n };
    stats.hist.unshift({ t: Date.now(), c: Z.daily ? 'daily' : Z.cat, s: Z.score, n: n });
    stats.hist = stats.hist.slice(0, 20);
    saveStats();
    var after = levelOf(stats.xp);

    var msg = pct === 100 ? 'Mashaalloh, a’lo natija!' : pct >= 70 ? 'Yaxshi natija!' : pct >= 40 ? 'Yomon emas, davom eting.' : 'Bilimni oshirishda davom eting.';
    var h = '<div class="card glass" style="text-align:center"><div class="muted small">Natija</div>' +
      '<div style="font-size:44px;font-weight:700;color:var(--gold2)">' + Z.score + ' / ' + n + '</div>' +
      '<div class="muted">' + pct + '% · ' + msg + '</div>' +
      '<div class="chip" style="margin-top:10px">+' + gained + ' ball</div>' +
      (after > before ? '<div style="margin-top:10px;font-weight:700;color:var(--gold2)">🎉 Yangi daraja: ' + esc(LEVELS[after].n) + '</div>' : '') + '</div>';
    h += levelHTML();
    if (!Z.daily) h += '<button class="btn" data-a="start" data-c="' + Z.cat + '">Qayta o‘ynash</button>';
    h += '<button class="btn ghost" data-a="menu">Menyuga qaytish</button>';
    var wasDaily = Z.daily;
    Z = null;
    el.innerHTML = h;
    window.scrollTo(0, 0);
    T.tg.haptic('success');
    if (wasDaily) T.toast('Kunlik sinov bajarildi');
  }

  /* ---------- SHAXSIY REYTING ---------- */
  function showRanking() {
    var tot = 0, ok = 0;
    Object.keys(stats.cat).forEach(function (k) { tot += stats.cat[k].t || 0; ok += stats.cat[k].c || 0; });
    var h = levelHTML();
    h += '<div class="card"><div class="row between"><div><div class="muted small">Javob berilgan savollar</div><b style="font-size:20px">' + tot + '</b></div>' +
      '<div style="text-align:right"><div class="muted small">To‘g‘ri javoblar</div><b style="font-size:20px">' + (tot ? Math.round(ok / tot * 100) + '%' : '—') + '</b></div></div></div>';

    h += '<div class="card"><div style="font-weight:600;margin-bottom:8px">Mavzular bo‘yicha</div>';
    CATS.forEach(function (c) {
      var s = stats.cat[c.id], p = s && s.t ? Math.round(s.c / s.t * 100) : 0;
      h += '<div class="row" style="gap:10px;padding:5px 0"><span class="small" style="width:100px">' + c.i + ' ' + esc(c.t) + '</span>' +
        '<div class="progress grow"><i style="width:' + p + '%"></i></div>' +
        '<b class="small" style="min-width:44px;text-align:right">' + (s && s.t ? p + '%' : '—') + '</b></div>';
    });
    h += '</div>';

    h += '<div class="card"><div style="font-weight:600;margin-bottom:8px">So‘nggi o‘yinlar</div>';
    if (!stats.hist.length) h += '<div class="src" style="margin-top:0">Hali o‘yin o‘ynalmadi.</div>';
    stats.hist.slice(0, 8).forEach(function (g) {
      var d = new Date(g.t);
      var name = g.c === 'daily' ? '🔥 Kunlik sinov' : g.c === 'mix' ? '🎲 Aralash' : catOf(g.c).i + ' ' + catOf(g.c).t;
      h += '<div class="row between small" style="padding:6px 0;border-bottom:1px solid var(--line)"><span>' + esc(name) +
        '<span class="muted"> · ' + d.getDate() + '.' + T.pad(d.getMonth() + 1) + '</span></span><b>' + g.s + ' / ' + g.n + '</b></div>';
    });
    h += '</div>';

    h += '<div class="card"><div class="src" style="margin-top:0">Bu — faqat sizning shaxsiy natijalaringiz va ular shu qurilmada saqlanadi. ' +
      'Boshqa foydalanuvchilar bilan umumiy reyting server (backend) ulangandan keyin qo‘shiladi. Hozircha soxta ro‘yxat ko‘rsatilmaydi.</div></div>';
    h += '<button class="btn" data-a="gotoquiz">Viktorinaga o‘tish</button>';
    el.innerHTML = h;
  }

  /* ---------- HODISALAR ---------- */
  function onClick(e) {
    var b = e.target.closest('[data-a]');
    if (!b) return;
    var a = b.getAttribute('data-a');
    if (a === 'start') startGame(b.getAttribute('data-c'));
    else if (a === 'ans') answer(+b.getAttribute('data-k'));
    else if (a === 'next') {
      if (!Z) return;
      if (Z.i + 1 < Z.qs.length) { Z.i++; Z.ans = -1; showQuestion(); window.scrollTo(0, 0); }
      else finish();
    }
    else if (a === 'menu') { showMenu(); }
    else if (a === 'gotoquiz') { T.app.open('quiz'); }
  }

  function mount(show) {
    return function (root) {
      el = root;
      stats = loadStats();
      Z = null;
      el.onclick = onClick;
      show();
    };
  }
  function leave() {
    if (el) el.onclick = null;
    el = null; Z = null;
  }

  T.sections.quiz = { title: 'Siyrat viktorinasi', icon: '🧠', render: mount(showMenu), leave: leave };
  T.sections.ranking = { title: 'Foydalanuvchilar reytingi', icon: '🏆', render: mount(showRanking), leave: leave };
})();
