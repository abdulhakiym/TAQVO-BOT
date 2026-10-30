/* TAQVO PRO MAX - adhkar.js (tonggi va kechgi zikrlar) */
(function () {
  'use strict';
  var T = window.TAQVO;

  var el = null, tab = 'morning', prog = null;

  function esc(s) { return T.esc(s); }
  function $(id) { return document.getElementById(id); }

  /* ---------- ZIKRLAR (faqat sahih va hasan) ---------- */
  var KURSI = {
    id: 'kursi', t: 'Oyatul Kursiy', n: 1,
    q: { type: 'ayah', ref: '2:255' },
    src: 'Qur’on, 2:255 (Baqara surasi). Fazilati haqidagi hadis: an-Nasoiy (‘Amal al-yavm val-layla’).',
    grade: 'sahih', gnote: 'Albaniy sahih degan (Sahih at-Targ‘ib)',
    tl: ''
  };
  var IKHLAS = {
    id: 'ikhlas', t: 'Ixlos surasi', n: 3,
    q: { type: 'surah', n: 112 },
    tl: 'Qul huvallohu ahad. Allohus-samad. Lam yalid va lam yulad. Va lam yakul-lahu kufuvan ahad.',
    src: 'Qur’on, 112. Abu Dovud 5082, Termiziy 3575: tong va kechda 3 martadan.',
    grade: 'hasan', gnote: 'Termiziy: hasan sahih g‘arib'
  };
  var FALAQ = {
    id: 'falaq', t: 'Falaq surasi', n: 3,
    q: { type: 'surah', n: 113 },
    tl: 'Qul a’uzu bi rabbil-falaq. Min sharri ma xalaq. Va min sharri g‘osiqin iza vaqab. Va min sharrin-naffasati fil-uqad. Va min sharri hasidin iza hasad.',
    src: 'Qur’on, 113. Abu Dovud 5082, Termiziy 3575: tong va kechda 3 martadan.',
    grade: 'hasan', gnote: 'Termiziy: hasan sahih g‘arib'
  };
  var NAS = {
    id: 'nas', t: 'Nos surasi', n: 3,
    q: { type: 'surah', n: 114 },
    tl: 'Qul a’uzu bi rabbin-nas. Malikin-nas. Ilahin-nas. Min sharril-vasvasil-xannas. Allazi yuvasvisu fi sudurin-nas. Minal-jinnati van-nas.',
    src: 'Qur’on, 114. Abu Dovud 5082, Termiziy 3575: tong va kechda 3 martadan.',
    grade: 'hasan', gnote: 'Termiziy: hasan sahih g‘arib'
  };

  var ISTIGHFAR = {
    id: 'istighfar', t: 'Sayyidul istig‘for', n: 1,
    ar: 'اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ لَكَ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ',
    tl: 'Allohumma anta rabbi, la ilaha illa anta, xalaqtani va ana abduka, va ana ala ahdika va va’dika mastato‘tu, a’uzu bika min sharri ma sana‘tu, abu’u laka bi ni’matika alayya, va abu’u laka bi zanbi fag‘fir li, fa innahu la yag‘firuz-zunuba illa anta.',
    mean: 'Ey Alloh, Sen mening Robbimsan, Sendan o‘zga iloh yo‘q. Meni Sen yaratding, men Sening bandangman va qodir bo‘lganimcha Senga bergan ahd va va’damda turaman. Qilgan yomonligimning sharridan Senga panoh tilayman. Menga bergan ne’matingni tan olaman va gunohimni ham tan olaman, meni mag‘firat qil, chunki gunohlarni Sendan o‘zga mag‘firat qiluvchi yo‘q.',
    src: 'Sahih al-Buxoriy 6306. Fazilati: kimki ishonib kunduzi aytsa va kechgacha vafot etsa, jannat ahlidan bo‘ladi (kechasi ham shunday).',
    grade: 'sahih', gnote: 'Sahih al-Buxoriy'
  };
  var RADIYTU = {
    id: 'radiytu', t: 'Robb, din va payg‘ambarga rozilik', n: 3,
    ar: 'رَضِيتُ بِاللَّهِ رَبًّا، وَبِالْإِسْلَامِ دِينًا، وَبِمُحَمَّدٍ نَبِيًّا',
    tl: 'Radiytu billahi rabban, va bil-islami dinan, va bi Muhammadin nabiyya.',
    mean: 'Alloh Robb ekaniga, Islom din ekaniga va Muhammad payg‘ambar ekaniga rozi bo‘ldim.',
    src: 'Abu Dovud 5072.',
    grade: 'hasan', gnote: 'Hasan'
  };
  var BISMILLAH = {
    id: 'bismillah', t: 'Zarar yetmaslik zikri', n: 3,
    ar: 'بِسْمِ اللَّهِ الَّذِي لَا يَضُرُّ مَعَ اسْمِهِ شَيْءٌ فِي الْأَرْضِ وَلَا فِي السَّمَاءِ وَهُوَ السَّمِيعُ الْعَلِيمُ',
    tl: 'Bismillahil-lazi la yadurru ma’asmihi shay’un fil-ardi va la fis-sama’i va huvas-sami’ul-alim.',
    mean: 'Ismi bilan yerda ham, osmonda ham hech narsa zarar yetkaza olmaydigan Alloh nomi bilan. U eshituvchi va biluvchidir.',
    src: 'Abu Dovud 5088, Termiziy 3388, Ibn Moja 3869: tong va kechda 3 martadan.',
    grade: 'hasan', gnote: 'Termiziy: hasan sahih g‘arib'
  };
  var ALIM = {
    id: 'alim', t: 'G‘oyibni biluvchi Alloh', n: 1,
    ar: 'اللَّهُمَّ عَالِمَ الْغَيْبِ وَالشَّهَادَةِ فَاطِرَ السَّمَاوَاتِ وَالْأَرْضِ، رَبَّ كُلِّ شَيْءٍ وَمَلِيكَهُ، أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا أَنْتَ، أَعُوذُ بِكَ مِنْ شَرِّ نَفْسِي وَمِنْ شَرِّ الشَّيْطَانِ وَشِرْكِهِ، وَأَنْ أَقْتَرِفَ عَلَى نَفْسِي سُوءًا أَوْ أَجُرَّهُ إِلَى مُسْلِمٍ',
    tl: 'Allohumma alimal-g‘aybi vash-shahadati fatiras-samavati val-ardi, rabba kulli shay’in va maliykah, ashhadu an la ilaha illa anta, a’uzu bika min sharri nafsi va min sharrish-shaytani va shirkih, va an aqtarifa ala nafsi su’an av ajurrahu ila muslim.',
    mean: 'Ey Alloh, g‘oyibni ham oshkorani ham biluvchi, osmonlar va yerni yaratuvchi, har narsaning Robbi va egasi, Sendan o‘zga iloh yo‘qligiga guvohlik beraman. Nafsimning yomonligidan, shayton va uning shirkining yomonligidan, o‘zimga yomonlik qilishdan yoki uni biror musulmonga yetkazishdan Senga panoh tilayman.',
    src: 'Abu Dovud 5067, Termiziy 3392.',
    grade: 'sahih', gnote: 'Termiziy: hasan sahih'
  };
  var SUBHAN = {
    id: 'subhan', t: 'Subhanallohi va bihamdih', n: 100,
    ar: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ',
    tl: 'Subhanallohi va bihamdih.',
    mean: 'Allohni (barcha kamchiliklardan) poklayman va Unga hamd aytaman.',
    src: 'Sahih Muslim 2692: tong va kechda 100 martadan.',
    grade: 'sahih', gnote: 'Sahih Muslim'
  };
  var LAILAHA = {
    id: 'lailaha', t: 'Tavhid zikri', n: 100,
    ar: 'لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ',
    tl: 'La ilaha illallohu vahdahu la sharika lah, lahul-mulku va lahul-hamdu va huva ala kulli shay’in qadir.',
    mean: 'Allohdan o‘zga iloh yo‘q, U yagona, Uning sherigi yo‘q. Mulk Unikidir, hamd Unikidir va U har narsaga qodirdir.',
    src: 'Sahih al-Buxoriy 3293, Sahih Muslim 2691: kun davomida 100 marta (vaqt tong bilan cheklanmagan).',
    grade: 'sahih', gnote: 'Sahih al-Buxoriy va Muslim'
  };
  var AFIYAH = {
    id: 'afiyah', t: 'Afv va omonlik duosi', n: 1,
    ar: 'اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَافِيَةَ فِي الدُّنْيَا وَالْآخِرَةِ، اللَّهُمَّ إِنِّي أَسْأَلُكَ الْعَفْوَ وَالْعَافِيَةَ فِي دِينِي وَدُنْيَايَ وَأَهْلِي وَمَالِي، اللَّهُمَّ اسْتُرْ عَوْرَاتِي وَآمِنْ رَوْعَاتِي، اللَّهُمَّ احْفَظْنِي مِنْ بَيْنِ يَدَيَّ وَمِنْ خَلْفِي وَعَنْ يَمِينِي وَعَنْ شِمَالِي وَمِنْ فَوْقِي، وَأَعُوذُ بِعَظَمَتِكَ أَنْ أُغْتَالَ مِنْ تَحْتِي',
    tl: 'Allohumma inni as’alukal-afiyata fid-dunya val-axira. Allohumma inni as’alukal-afva val-afiyata fi dini va dunyaya va ahli va mali. Allohumma ustur avrati va amin ravati. Allohumma ihfazni min bayni yadayya va min xalfi va an yamini va an shimali va min fawqi, va a’uzu bi azamatika an ugtala min tahti.',
    mean: 'Ey Alloh, dunyo va oxiratda omonlik so‘rayman. Ey Alloh, dinim, dunyoyim, oilam va molimda afv va omonlik so‘rayman. Ey Alloh, aybimni berkit va qo‘rquvlarimdan omon qil. Ey Alloh, meni oldimdan, ortimdan, o‘ngimdan, so‘limdan va ustimdan asra. Tagimdan (yerga yutilib) halok qilinishdan Sening azamating bilan panoh tilayman.',
    src: 'Abu Dovud 5074, Ibn Moja 3871.',
    grade: 'sahih', gnote: 'Albaniy sahih degan'
  };

  var ASBAHNA = {
    id: 'asbahna', t: 'Tong zikri: mulk Allohniki', n: 1,
    ar: 'أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، رَبِّ أَسْأَلُكَ خَيْرَ مَا فِي هَذَا الْيَوْمِ وَخَيْرَ مَا بَعْدَهُ، وَأَعُوذُ بِكَ مِنْ شَرِّ مَا فِي هَذَا الْيَوْمِ وَشَرِّ مَا بَعْدَهُ، رَبِّ أَعُوذُ بِكَ مِنَ الْكَسَلِ وَسُوءِ الْكِبَرِ، رَبِّ أَعُوذُ بِكَ مِنْ عَذَابٍ فِي النَّارِ وَعَذَابٍ فِي الْقَبْرِ',
    tl: 'Asbahna va asbahal-mulku lillah, val-hamdu lillah, la ilaha illallohu vahdahu la sharika lah, lahul-mulku va lahul-hamdu va huva ala kulli shay’in qadir. Rabbi as’aluka xayra ma fi hazal-yavmi va xayra ma ba’dah, va a’uzu bika min sharri ma fi hazal-yavmi va sharri ma ba’dah. Rabbi a’uzu bika minal-kasali va su’il-kibar. Rabbi a’uzu bika min azabin fin-nari va azabin fil-qabr.',
    mean: 'Tong ottirdik va mulk Allohniki bo‘lib tong otdi. Hamd Allohgadir. Allohdan o‘zga iloh yo‘q, U yagona, sherigi yo‘q. Mulk Unikidir, hamd Unikidir va U har narsaga qodirdir. Robbim, bugungi kundagi yaxshilikni va undan keyingi yaxshilikni Sendan so‘rayman; bugungi kundagi yomonlikdan va undan keyingi yomonlikdan Senga panoh tilayman. Robbim, erinchoqlikdan va keksalikning yomonligidan Senga panoh tilayman. Robbim, do‘zax azobidan va qabr azobidan Senga panoh tilayman.',
    src: 'Sahih Muslim 2723.',
    grade: 'sahih', gnote: 'Sahih Muslim'
  };
  var AMSAYNA = {
    id: 'amsayna', t: 'Kech zikri: mulk Allohniki', n: 1,
    ar: 'أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ، وَالْحَمْدُ لِلَّهِ، لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ، رَبِّ أَسْأَلُكَ خَيْرَ مَا فِي هَذِهِ اللَّيْلَةِ وَخَيْرَ مَا بَعْدَهَا، وَأَعُوذُ بِكَ مِنْ شَرِّ مَا فِي هَذِهِ اللَّيْلَةِ وَشَرِّ مَا بَعْدَهَا، رَبِّ أَعُوذُ بِكَ مِنَ الْكَسَلِ وَسُوءِ الْكِبَرِ، رَبِّ أَعُوذُ بِكَ مِنْ عَذَابٍ فِي النَّارِ وَعَذَابٍ فِي الْقَبْرِ',
    tl: 'Amsayna va amsal-mulku lillah, val-hamdu lillah, la ilaha illallohu vahdahu la sharika lah, lahul-mulku va lahul-hamdu va huva ala kulli shay’in qadir. Rabbi as’aluka xayra ma fi hazihil-laylati va xayra ma ba’daha, va a’uzu bika min sharri ma fi hazihil-laylati va sharri ma ba’daha. Rabbi a’uzu bika minal-kasali va su’il-kibar. Rabbi a’uzu bika min azabin fin-nari va azabin fil-qabr.',
    mean: 'Kech kirdik va mulk Allohniki bo‘lib kech kirdi. Hamd Allohgadir. Allohdan o‘zga iloh yo‘q, U yagona, sherigi yo‘q. Mulk Unikidir, hamd Unikidir va U har narsaga qodirdir. Robbim, shu tundagi yaxshilikni va undan keyingi yaxshilikni Sendan so‘rayman; shu tundagi yomonlikdan va undan keyingi yomonlikdan Senga panoh tilayman. Robbim, erinchoqlikdan va keksalikning yomonligidan Senga panoh tilayman. Robbim, do‘zax azobidan va qabr azobidan Senga panoh tilayman.',
    src: 'Sahih Muslim 2723.',
    grade: 'sahih', gnote: 'Sahih Muslim'
  };
  var BIKA_M = {
    id: 'bikam', t: 'Sening ne’mating bilan tong ottirdik', n: 1,
    ar: 'اللَّهُمَّ بِكَ أَصْبَحْنَا، وَبِكَ أَمْسَيْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ النُّشُورُ',
    tl: 'Allohumma bika asbahna, va bika amsayna, va bika nahya, va bika namutu, va ilaykan-nushur.',
    mean: 'Ey Alloh, Sening (ne’mating va irodang) bilan tong ottirdik, Sening (ne’mating va irodang) bilan kech kirdik, Sening (irodang) bilan tirilamiz va o‘lamiz, qayta tirilish Sengadir.',
    src: 'Abu Dovud 5068, Termiziy 3391.',
    grade: 'hasan', gnote: 'Termiziy: hasan'
  };
  var BIKA_E = {
    id: 'bikae', t: 'Sening ne’mating bilan kech kirdik', n: 1,
    ar: 'اللَّهُمَّ بِكَ أَمْسَيْنَا، وَبِكَ أَصْبَحْنَا، وَبِكَ نَحْيَا، وَبِكَ نَمُوتُ، وَإِلَيْكَ الْمَصِيرُ',
    tl: 'Allohumma bika amsayna, va bika asbahna, va bika nahya, va bika namutu, va ilaykal-masir.',
    mean: 'Ey Alloh, Sening (ne’mating va irodang) bilan kech kirdik, Sening (ne’mating va irodang) bilan tong ottirdik, Sening (irodang) bilan tirilamiz va o‘lamiz, qaytish Sengadir.',
    src: 'Abu Dovud 5068, Termiziy 3391.',
    grade: 'hasan', gnote: 'Termiziy: hasan'
  };
  var AUZU = {
    id: 'auzu', t: 'Alloh kalimalari bilan panoh', n: 3,
    ar: 'أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ مِنْ شَرِّ مَا خَلَقَ',
    tl: 'A’uzu bi kalimatillahit-tammati min sharri ma xalaq.',
    mean: 'Allohning komil kalimalari bilan U yaratgan narsalarning yomonligidan panoh tilayman.',
    src: 'Termiziy 3604: kechqurun 3 marta aytgan kishiga o‘sha tunda zahar zarar qilmaydi.',
    grade: 'hasan', gnote: 'Termiziy: hasan'
  };

  var LISTS = {
    morning: [KURSI, IKHLAS, FALAQ, NAS, ASBAHNA, BIKA_M, ALIM, ISTIGHFAR, RADIYTU, BISMILLAH, SUBHAN, LAILAHA, AFIYAH],
    evening: [KURSI, IKHLAS, FALAQ, NAS, AMSAYNA, BIKA_E, ALIM, ISTIGHFAR, RADIYTU, BISMILLAH, SUBHAN, AUZU, AFIYAH]
  };

  /* ---------- KIRILL -> LOTIN (Qur'on tarjimasi uchun) ---------- */
  var C2L = { 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ё': 'yo', 'ж': 'j', 'з': 'z', 'и': 'i', 'й': 'y',
    'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
    'х': 'x', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '\u02BC', 'ь': '', 'ы': 'i', 'э': 'e',
    'ю': 'yu', 'я': 'ya', 'ў': 'o\u02BB', 'қ': 'q', 'ғ': 'g\u02BB', 'ҳ': 'h' };
  var VOW = 'аеёиоуўэюяъ';
  function lat(s) {
    var out = '';
    for (var i = 0; i < s.length; i++) {
      var ch = s.charAt(i), lo = ch.toLowerCase(), up = ch !== lo, v;
      if (lo === 'е') {
        var p = i > 0 ? s.charAt(i - 1).toLowerCase() : ' ';
        v = (!/[\u0400-\u04FF]/.test(p) || VOW.indexOf(p) > -1) ? 'ye' : 'e';
      } else v = C2L[lo];
      if (v === undefined) { out += ch; continue; }
      out += (up && v.length) ? v.charAt(0).toUpperCase() + v.slice(1) : v;
    }
    return out;
  }
  function stripDia(s) { return String(s).replace(/[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/g, ''); }

  /* ---------- QUR'ON MATNINI OLISH ---------- */
  function api(path) {
    return T.cachedJSON(T.config.QURAN + path, 30 * 24 * 3600 * 1000, { timeout: 15000, retries: 1 })
      .then(function (res) {
        if (!res || res.code !== 200 || !res.data) throw new Error('bad');
        return res.data;
      });
  }
  function fetchQ(q) {
    var base = q.type === 'ayah' ? '/ayah/' + q.ref : '/surah/' + q.n;
    return api(base + '/editions/quran-uthmani,uz.sodik').catch(function () {
      return api(base + '/quran-uthmani').then(function (d) { return [d]; });
    }).then(function (d) {
      var ar, tr = '', ed = null;
      if (q.type === 'ayah') {
        ar = d[0].text;
        if (d[1]) { tr = d[1].text; ed = d[1].edition; }
      } else {
        var a0 = d[0].ayahs.map(function (a, i) {
          var t = a.text;
          if (i === 0 && a.numberInSurah === 1) {
            var w = t.split(' ');
            if (w.length > 4 && stripDia(w[0]) === 'بسم') t = w.slice(4).join(' ');
          }
          return t;
        });
        ar = a0.join(' ');
        if (d[1]) { tr = d[1].ayahs.map(function (a) { return a.text; }).join(' '); ed = d[1].edition; }
      }
      if (tr && /[\u0400-\u04FF]/.test(tr)) tr = lat(tr);
      return { ar: ar, tr: tr, ed: ed };
    });
  }
  function fillQuran(it) {
    var box = $('qt-' + it.id);
    if (!box) return;
    fetchQ(it.q).then(function (r) {
      var b = $('qt-' + it.id);
      if (!b) return;
      b.innerHTML = '<div class="arabic">' + esc(r.ar) + '</div>' +
        (it.tl ? '<div class="translit">' + esc(it.tl) + '</div>' : '') +
        (r.tr ? '<div class="meaning">' + esc(r.tr) + '</div>' +
          '<div class="src">Tarjima: ' + esc((r.ed && (r.ed.englishName || r.ed.name)) || 'uz.sodik') + ' (Al Quran Cloud). Lotin yozuvi avtomatik, taxminiy bo‘lishi mumkin.</div>'
          : '<div class="src">O‘zbekcha tarjima yuklanmadi. Matn: Al Quran Cloud.</div>');
    }).catch(function () {
      var b = $('qt-' + it.id);
      if (b) b.innerHTML = T.errorHTML('Qur’on matnini yuklab bo‘lmadi', 'adRetry');
    });
  }

  /* ---------- TARAQQIYOT ---------- */
  function today() {
    var d = new Date();
    return d.getFullYear() + '-' + T.pad(d.getMonth() + 1) + '-' + T.pad(d.getDate());
  }
  function loadProg() {
    var p = T.store.get('adhkar:prog', null);
    if (!p || p.d !== today() || !p.morning || !p.evening) p = { d: today(), morning: {}, evening: {} };
    return p;
  }
  function saveProg() { T.store.set('adhkar:prog', prog); }
  function cnt(it) { return prog[tab][it.id] || 0; }
  function find(id) {
    var l = LISTS[tab];
    for (var i = 0; i < l.length; i++) if (l[i].id === id) return l[i];
    return null;
  }

  /* ---------- KO'RINISH ---------- */
  function gradeChip(it) {
    var cls = it.grade === 'sahih' ? 'sahih' : 'hasan';
    var name = it.grade === 'sahih' ? 'Sahih' : 'Hasan';
    return '<span class="chip ' + cls + '">' + name + '</span>' +
      (it.gnote ? ' <span class="small muted">' + esc(it.gnote) + '</span>' : '');
  }

  function footHTML(it) {
    var c = cnt(it), done = c >= it.n;
    var label = it.n === 1 ? (done ? '✓ O‘qildi' : 'O‘qidim') : (done ? '✓ Bajarildi' : '+1');
    return '<div class="row between" style="margin-top:10px;gap:8px">' +
      '<span class="chip' + (done ? ' sahih' : '') + '">' + (it.n > 1 ? c + ' / ' + it.n : (done ? 'Bajarildi' : '1 marta')) + '</span>' +
      '<span class="row" style="gap:6px">' +
      '<button class="btn sm' + (done ? ' ghost' : '') + '" data-a="tap" data-id="' + it.id + '"' + (done ? ' disabled style="opacity:.7"' : '') + '>' + label + '</button>' +
      '<button class="icon-btn" data-a="rst" data-id="' + it.id + '" title="Qayta">↺</button></span></div>' +
      (it.n > 1 ? '<div class="progress" style="margin-top:8px"><i style="width:' + Math.min(100, Math.round(c / it.n * 100)) + '%"></i></div>' : '');
  }

  function topHTML() {
    var l = LISTS[tab], done = 0;
    l.forEach(function (it) { if (cnt(it) >= it.n) done++; });
    var pct = Math.round(done / l.length * 100);
    return '<div class="row between"><b>' + (tab === 'morning' ? 'Tonggi zikrlar' : 'Kechgi zikrlar') + '</b>' +
      '<span class="chip' + (done === l.length ? ' sahih' : '') + '">' + done + ' / ' + l.length + (done === l.length ? ' ✓' : '') + '</span></div>' +
      '<div class="progress" style="margin-top:10px"><i style="width:' + pct + '%"></i></div>' +
      '<div class="src">' + (tab === 'morning'
        ? 'Odatda Bomdoddan keyin, kun ko‘tarilguncha o‘qiladi.'
        : 'Odatda Asrdan keyin, Shomgacha yoki kechgacha o‘qiladi.') + ' Holat har kuni yangilanadi.</div>';
  }

  function render() {
    var l = LISTS[tab], h = '';
    h += '<div class="tabs"><button class="tab' + (tab === 'morning' ? ' active' : '') + '" data-a="tab" data-t="morning">🌅 Tonggi zikrlar</button>' +
         '<button class="tab' + (tab === 'evening' ? ' active' : '') + '" data-a="tab" data-t="evening">🌙 Kechgi zikrlar</button></div>';
    h += '<div class="card glass" id="adTop">' + topHTML() + '</div>';

    l.forEach(function (it, i) {
      h += '<div class="card" id="ad-' + it.id + '"><div class="row between"><b>' + (i + 1) + '. ' + esc(it.t) + '</b></div>';
      if (it.q) {
        h += '<div id="qt-' + it.id + '">' + T.loaderHTML + '</div>';
      } else {
        h += '<div class="arabic">' + esc(it.ar) + '</div>' +
          '<div class="translit">' + esc(it.tl) + '</div>' +
          '<div class="meaning">' + esc(it.mean) + '</div>';
      }
      h += '<div class="src" style="margin-top:10px">Manba: ' + esc(it.src) + '</div>';
      h += '<div style="margin-top:6px">' + gradeChip(it) + '</div>';
      h += '<div id="ft-' + it.id + '">' + footHTML(it) + '</div></div>';
    });

    h += '<div class="card"><div class="src" style="margin-top:0">' +
      'Eslatma: bu bo‘lim ta’limiy maqsadda. Ma’no tarjimalari ma’no jihatidan berilgan. ' +
      'Faqat sahih va hasan darajadagi rivoyatlar kiritilgan, zaif rivoyatlar ataylab qo‘shilmagan. ' +
      'Hadis raqamlari turli nashrlarda farq qilishi mumkin, ishonchli manbada (masalan, sunnah.com) solishtirib ko‘ring.</div></div>';

    el.innerHTML = h;
    l.forEach(function (it) { if (it.q) fillQuran(it); });
  }

  function refreshItem(it) {
    var f = $('ft-' + it.id);
    if (f) f.innerHTML = footHTML(it);
    var t = $('adTop');
    if (t) t.innerHTML = topHTML();
  }

  /* ---------- HODISALAR ---------- */
  function onClick(e) {
    if (e.target.id === 'adRetry') { render(); return; }
    var b = e.target.closest('[data-a]');
    if (!b) return;
    var a = b.getAttribute('data-a');
    if (a === 'tab') {
      tab = b.getAttribute('data-t');
      T.store.set('adhkar:tab', tab);
      render();
      window.scrollTo(0, 0);
      return;
    }
    var it = find(b.getAttribute('data-id'));
    if (!it) return;
    if (a === 'tap') {
      var c = cnt(it);
      if (c >= it.n) return;
      prog[tab][it.id] = c + 1;
      saveProg();
      if (c + 1 >= it.n) {
        T.tg.haptic('success');
        T.toast('Bajarildi ✓');
      } else {
        T.tg.haptic('light');
      }
      refreshItem(it);
    } else if (a === 'rst') {
      prog[tab][it.id] = 0;
      saveProg();
      refreshItem(it);
    }
  }

  T.sections.adhkar = {
    title: 'Tonggi va kechgi zikrlar',
    icon: '🌅',
    render: function (root) {
      el = root;
      prog = loadProg();
      var saved = T.store.get('adhkar:tab', null);
      if (saved === 'morning' || saved === 'evening') tab = saved;
      else tab = new Date().getHours() < 14 ? 'morning' : 'evening';
      el.onclick = onClick;
      render();
    },
    leave: function () {
      if (el) el.onclick = null;
      el = null;
    }
  };
})();
