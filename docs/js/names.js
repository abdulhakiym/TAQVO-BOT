/* TAQVO PRO MAX - names.js (Allohning 99 go'zal ismi) */
(function () {
  'use strict';
  var T = window.TAQVO;

  // [arabcha, o'qilishi, o'zbekcha ma'no]; raqami = tartibi (1..99)
  var N = [
    ['ٱلرَّحْمَٰنُ', 'Ar-Rohman', 'Cheksiz rahmli. Rahmati barcha maxluqotni qamrab olgan.'],
    ['ٱلرَّحِيمُ', 'Ar-Rohim', 'Mo‘minlarga alohida mehribon, rahm qiluvchi.'],
    ['ٱلْمَلِكُ', 'Al-Malik', 'Barcha narsaning haqiqiy egasi va podshohi.'],
    ['ٱلْقُدُّوسُ', 'Al-Quddus', 'Har qanday nuqson va kamchilikdan pok.'],
    ['ٱلسَّلَامُ', 'As-Salom', 'Har qanday ayb-nuqsondan salomat; omonlik beruvchi.'],
    ['ٱلْمُؤْمِنُ', 'Al-Mu’min', 'Bandalariga omonlik beruvchi; va’dasini tasdiqlovchi.'],
    ['ٱلْمُهَيْمِنُ', 'Al-Muhaymin', 'Hamma narsani kuzatib va asrab turuvchi.'],
    ['ٱلْعَزِيزُ', 'Al-Aziz', 'Yengilmas, mutlaq izzat va qudrat egasi.'],
    ['ٱلْجَبَّارُ', 'Al-Jabbor', 'Irodasi hamma ustidan o‘tuvchi; singanni tuzatuvchi.'],
    ['ٱلْمُتَكَبِّرُ', 'Al-Mutakabbir', 'Haqiqiy ulug‘lik va buyuklik faqat Unga xos.'],
    ['ٱلْخَالِقُ', 'Al-Xoliq', 'Yo‘qdan bor qiluvchi, yaratuvchi.'],
    ['ٱلْبَارِئُ', 'Al-Bori’', 'Maxluqotni nuqsonsiz, uyg‘un qilib paydo qiluvchi.'],
    ['ٱلْمُصَوِّرُ', 'Al-Musavvir', 'Maxluqotlarga shakl va suvrat beruvchi.'],
    ['ٱلْغَفَّارُ', 'Al-G‘offor', 'Gunohlarni qayta-qayta kechiruvchi.'],
    ['ٱلْقَهَّارُ', 'Al-Qohhor', 'Hamma narsa ustidan g‘olib va qahr qiluvchi.'],
    ['ٱلْوَهَّابُ', 'Al-Vahhob', 'Evaziga hech narsa so‘ramay mo‘l in’om qiluvchi.'],
    ['ٱلرَّزَّاقُ', 'Ar-Rozzoq', 'Barcha maxluqotga rizq beruvchi.'],
    ['ٱلْفَتَّاحُ', 'Al-Fattoh', 'Rahmat va rizq eshiklarini ochuvchi; haq hukm qiluvchi.'],
    ['ٱلْعَلِيمُ', 'Al-Alim', 'Hamma narsani biluvchi.'],
    ['ٱلْقَابِضُ', 'Al-Qobid', 'Istagan kishisiga rizqni qisuvchi, toraytiruvchi.'],
    ['ٱلْبَاسِطُ', 'Al-Bosit', 'Istagan kishisiga rizqni kengaytiruvchi.'],
    ['ٱلْخَافِضُ', 'Al-Xofid', 'Istaganini (adolat bilan) pastga tushiruvchi.'],
    ['ٱلرَّافِعُ', 'Ar-Rofi’', 'Istaganini ko‘taruvchi, martabasini oshiruvchi.'],
    ['ٱلْمُعِزُّ', 'Al-Mu’izz', 'Istaganiga izzat beruvchi.'],
    ['ٱلْمُذِلُّ', 'Al-Muzill', 'Istaganini (adolat bilan) xor qiluvchi.'],
    ['ٱلسَّمِيعُ', 'As-Sami’', 'Hamma narsani eshituvchi.'],
    ['ٱلْبَصِيرُ', 'Al-Basir', 'Hamma narsani ko‘ruvchi.'],
    ['ٱلْحَكَمُ', 'Al-Hakam', 'Haq hukm chiqaruvchi hakam.'],
    ['ٱلْعَدْلُ', 'Al-Adl', 'Mutlaq adolatli.'],
    ['ٱللَّطِيفُ', 'Al-Latif', 'Lutfkor; eng nozik narsalardan ham xabardor.'],
    ['ٱلْخَبِيرُ', 'Al-Xabir', 'Hamma narsaning ichki haqiqatidan to‘liq xabardor.'],
    ['ٱلْحَلِيمُ', 'Al-Halim', 'Bardoshli; jazolashga shoshilmaydigan.'],
    ['ٱلْعَظِيمُ', 'Al-Azim', 'Buyuk, ulug‘vor.'],
    ['ٱلْغَفُورُ', 'Al-G‘ofur', 'Ko‘p kechiruvchi.'],
    ['ٱلشَّكُورُ', 'Ash-Shakur', 'Oz amalga ham katta mukofot beruvchi, qadrlovchi.'],
    ['ٱلْعَلِيُّ', 'Al-Aliy', 'Oliy, hamma narsadan yuksak.'],
    ['ٱلْكَبِيرُ', 'Al-Kabir', 'Eng katta, eng ulug‘.'],
    ['ٱلْحَفِيظُ', 'Al-Hafiz', 'Hamma narsani saqlovchi va asrovchi.'],
    ['ٱلْمُقِيتُ', 'Al-Muqit', 'Har bir jonzotga ozuqa va qudrat beruvchi; kuzatib turuvchi.'],
    ['ٱلْحَسِيبُ', 'Al-Hasib', 'Bandalariga kifoya qiluvchi; hisob oluvchi.'],
    ['ٱلْجَلِيلُ', 'Al-Jalil', 'Ulug‘vorlik va azamat sifatlari egasi.'],
    ['ٱلْكَرِيمُ', 'Al-Karim', 'Saxovatli, karam egasi.'],
    ['ٱلرَّقِيبُ', 'Ar-Roqib', 'Hamma narsani doimiy kuzatib turuvchi.'],
    ['ٱلْمُجِيبُ', 'Al-Mujib', 'Duoni ijobat qiluvchi.'],
    ['ٱلْوَاسِعُ', 'Al-Vosi’', 'Rahmati, ilmi va fazli keng.'],
    ['ٱلْحَكِيمُ', 'Al-Hakim', 'Hikmat egasi; har ishni o‘rniga qo‘yuvchi.'],
    ['ٱلْوَدُودُ', 'Al-Vadud', 'Solih bandalarini sevuvchi va sevilishga loyiq.'],
    ['ٱلْمَجِيدُ', 'Al-Majid', 'Shon-sharafi buyuk va keng.'],
    ['ٱلْبَاعِثُ', 'Al-Bo’is', 'Qiyomatda o‘liklarni qayta tiriltiruvchi.'],
    ['ٱلشَّهِيدُ', 'Ash-Shahid', 'Hamma narsaga guvoh.'],
    ['ٱلْحَقُّ', 'Al-Haqq', 'Haq; mavjudligi shak-shubhasiz.'],
    ['ٱلْوَكِيلُ', 'Al-Vakil', 'Ishlarni topshirishga eng ishonchli zot.'],
    ['ٱلْقَوِيُّ', 'Al-Qaviy', 'Kuch-qudrat egasi.'],
    ['ٱلْمَتِينُ', 'Al-Matin', 'Qudrati mustahkam, zaiflik Unga yo‘q.'],
    ['ٱلْوَلِيُّ', 'Al-Valiy', 'Mo‘minlarning do‘sti va yordamchisi.'],
    ['ٱلْحَمِيدُ', 'Al-Hamid', 'Hamd va sanoga loyiq.'],
    ['ٱلْمُحْصِي', 'Al-Muhsi', 'Hamma narsani sanog‘i bilan biluvchi.'],
    ['ٱلْمُبْدِئُ', 'Al-Mubdi’', 'Maxluqotni birinchi marta paydo qiluvchi.'],
    ['ٱلْمُعِيدُ', 'Al-Mu’id', 'Maxluqotni qayta tiriltiruvchi.'],
    ['ٱلْمُحْيِي', 'Al-Muhyi', 'Hayot beruvchi.'],
    ['ٱلْمُمِيتُ', 'Al-Mumit', 'O‘lim beruvchi.'],
    ['ٱلْحَيُّ', 'Al-Hayy', 'Abadiy tirik.'],
    ['ٱلْقَيُّومُ', 'Al-Qayyum', 'O‘zi mustaqil turuvchi va hamma narsani tutib turuvchi.'],
    ['ٱلْوَاجِدُ', 'Al-Vojid', 'Xohlagan narsasini topuvchi; Unga hech narsa yetishmaydi.'],
    ['ٱلْمَاجِدُ', 'Al-Mojid', 'Ulug‘vor, shon-sharaf egasi.'],
    ['ٱلْوَاحِدُ', 'Al-Vohid', 'Yagona.'],
    ['ٱلْأَحَدُ', 'Al-Ahad', 'Yakka-yu yagona, o‘xshashi yo‘q.'],
    ['ٱلصَّمَدُ', 'As-Samad', 'Hamma Unga muhtoj, O‘zi esa hech kimga muhtoj emas.'],
    ['ٱلْقَادِرُ', 'Al-Qodir', 'Hamma narsaga qodir.'],
    ['ٱلْمُقْتَدِرُ', 'Al-Muqtadir', 'Mutlaq qudrat egasi.'],
    ['ٱلْمُقَدِّمُ', 'Al-Muqaddim', 'Istaganini oldinga o‘tkazuvchi.'],
    ['ٱلْمُؤَخِّرُ', 'Al-Mu’axxir', 'Istaganini ortga suruvchi.'],
    ['ٱلْأَوَّلُ', 'Al-Avval', 'Boshlanishi yo‘q; hammadan oldin.'],
    ['ٱلْآخِرُ', 'Al-Oxir', 'Oxiri yo‘q; hamma narsadan keyin ham qoluvchi.'],
    ['ٱلظَّاهِرُ', 'Az-Zohir', 'Zohir; dalillari oshkor, hamma narsadan yuqori.'],
    ['ٱلْبَاطِنُ', 'Al-Botin', 'Botin; hamma sirdan xabardor.'],
    ['ٱلْوَالِي', 'Al-Voli', 'Barcha ishlarni boshqaruvchi.'],
    ['ٱلْمُتَعَالِي', 'Al-Muta’oli', 'Hamma narsadan yuksak va ustun.'],
    ['ٱلْبَرُّ', 'Al-Barr', 'Yaxshilik qiluvchi, mehribon.'],
    ['ٱلتَّوَّابُ', 'At-Tavvob', 'Tavbani ko‘p qabul qiluvchi.'],
    ['ٱلْمُنْتَقِمُ', 'Al-Muntaqim', 'Zolimlardan adolat bilan jazo oluvchi.'],
    ['ٱلْعَفُوُّ', 'Al-Afuv', 'Ko‘p afv qiluvchi, gunohlarni o‘chirib yuboruvchi.'],
    ['ٱلرَّءُوفُ', 'Ar-Ro’uf', 'O‘ta shafqatli.'],
    ['مَالِكُ ٱلْمُلْكِ', 'Molikul-Mulk', 'Mulkning egasi.'],
    ['ذُو ٱلْجَلَالِ وَٱلْإِكْرَامِ', 'Zul-Jalali val-Ikrom', 'Ulug‘vorlik va ikrom egasi.'],
    ['ٱلْمُقْسِطُ', 'Al-Muqsit', 'Adolatli; har kimning haqqini to‘la beruvchi.'],
    ['ٱلْجَامِعُ', 'Al-Jomi’', 'Qiyomatda maxluqotni to‘plovchi.'],
    ['ٱلْغَنِيُّ', 'Al-G‘aniy', 'Hech narsaga muhtoj bo‘lmagan.'],
    ['ٱلْمُغْنِي', 'Al-Mug‘niy', 'Istagan kishisini boy va behojat qiluvchi.'],
    ['ٱلْمَانِعُ', 'Al-Moni’', 'Hikmati bilan istagan narsasidan to‘suvchi va asrovchi.'],
    ['ٱلضَّارُّ', 'Az-Zorr', 'Hikmati bilan zarar (sinov) yetkazishga qodir. Odatda «An-Nofi’» bilan birga zikr qilinadi.'],
    ['ٱلنَّافِعُ', 'An-Nofi’', 'Foyda beruvchi.'],
    ['ٱلنُّورُ', 'An-Nur', 'Osmonlar va yerning nuri; hidoyat nuri beruvchi.'],
    ['ٱلْهَادِي', 'Al-Hodiy', 'Hidoyat qiluvchi, to‘g‘ri yo‘lga boshlovchi.'],
    ['ٱلْبَدِيعُ', 'Al-Badi’', 'Misli yo‘q holda yaratuvchi.'],
    ['ٱلْبَاقِي', 'Al-Boqi', 'Abadiy qoluvchi.'],
    ['ٱلْوَارِثُ', 'Al-Vorith', 'Hamma narsa fano bo‘lgach, qoluvchi vorus.'],
    ['ٱلرَّشِيدُ', 'Ar-Rashid', 'Bandalarini to‘g‘ri yo‘lga yo‘llovchi.'],
    ['ٱلصَّبُورُ', 'As-Sabur', 'Sabrli; jazolashga shoshilmaydigan.']
  ];

  var S = { q: '', tab: 'all' };
  var el = null;

  /* ---------- YORDAMCHI ---------- */
  function esc(s) { return T.esc(s); }
  function $(id) { return document.getElementById(id); }
  function stripDia(s) { return String(s).replace(/[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/g, ''); }
  function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9\u0400-\u04FF]/g, ''); }
  function favs() {
    var f = T.store.get('names:fav', []);
    return Array.isArray(f) ? f : [];
  }
  function isFav(n) { return favs().indexOf(n) > -1; }
  function toggleFav(n) {
    var f = favs(), i = f.indexOf(n);
    if (i > -1) f.splice(i, 1); else f.push(n);
    T.store.set('names:fav', f);
    return i === -1;
  }
  function dayIndex() {
    var d = new Date();
    return Math.floor(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000) % 99;
  }

  /* ---------- KO'RINISH ---------- */
  function cardHTML(n) {
    var d = N[n - 1], fav = isFav(n);
    return '<div class="card" data-n="' + n + '">' +
      '<div class="row between"><span class="num">' + n + '</span><span class="row" style="gap:6px">' +
      '<button class="icon-btn" data-a="share" data-n="' + n + '">↗</button>' +
      '<button class="icon-btn' + (fav ? ' on' : '') + '" data-a="fav" data-n="' + n + '">' + (fav ? '★' : '☆') + '</button></span></div>' +
      '<div class="arabic" style="text-align:center;font-size:36px;line-height:1.8;color:var(--gold2)">' + esc(d[0]) + '</div>' +
      '<div style="text-align:center;font-weight:600;margin-top:2px">' + esc(d[1]) + '</div>' +
      '<div class="meaning" style="text-align:center">' + esc(d[2]) + '</div></div>';
  }

  function matches(n, q, raw) {
    var d = N[n - 1];
    if (!q && !raw) return true;
    if (q && (String(n) === q || norm(d[1]).indexOf(q) > -1 || norm(d[2]).indexOf(q) > -1)) return true;
    return !!raw && stripDia(d[0]).indexOf(raw) > -1;
  }

  function renderList() {
    var box = $('nmList');
    if (!box) return;
    var q = norm(S.q), raw = stripDia(S.q.trim());
    var f = favs(), out = [];
    for (var n = 1; n <= 99; n++) {
      if (S.tab === 'fav' && f.indexOf(n) === -1) continue;
      if (matches(n, q, raw)) out.push(n);
    }
    if (!out.length) {
      box.innerHTML = '<div class="empty">' + (S.tab === 'fav' && !f.length
        ? 'Hali sevimli ism yo‘q.<br>Ism yonidagi ☆ tugmasini bosing.'
        : 'Hech narsa topilmadi.') + '</div>';
    } else {
      box.innerHTML = out.map(cardHTML).join('');
    }
    var c = $('nmCount');
    if (c) c.textContent = out.length + ' ta ism';
    var ft = $('nmFavTab');
    if (ft) ft.textContent = '★ Sevimlilar (' + f.length + ')';
  }

  function renderAll() {
    var di = dayIndex() + 1, d = N[di - 1], h = '';
    h += '<div class="card glass" style="text-align:center">' +
      '<div class="muted small">Kunning ismi · ' + di + '-ism</div>' +
      '<div class="arabic" style="text-align:center;font-size:42px;line-height:1.7;color:var(--gold2)">' + esc(d[0]) + '</div>' +
      '<div style="font-weight:700;font-size:18px">' + esc(d[1]) + '</div>' +
      '<div class="meaning">' + esc(d[2]) + '</div></div>';

    h += '<input type="search" id="nmSearch" placeholder="Qidirish: raqam, nom yoki ma’no…" autocomplete="off">';
    h += '<div class="tabs"><button class="tab' + (S.tab === 'all' ? ' active' : '') + '" data-a="tab" data-t="all">Barchasi</button>' +
      '<button class="tab' + (S.tab === 'fav' ? ' active' : '') + '" data-a="tab" data-t="fav" id="nmFavTab">★ Sevimlilar</button></div>';
    h += '<div class="muted small" id="nmCount"></div>';
    h += '<div id="nmList" style="display:flex;flex-direction:column;gap:12px"></div>';

    h += '<div class="card"><div class="src" style="margin-top:0">' +
      'Eslatma: «Alloh Taoloning to‘qson to‘qqizta ismi bor, kim ularni (ihso qilsa) yod olsa va ularga amal qilsa jannatga kiradi» mazmunidagi hadis ' +
      'Sahih al-Buxoriy (2736) va Sahih Muslim (2677) da keladi. ' +
      'Ismlarni birma-bir sanab o‘tgan ro‘yxat esa Termiziy rivoyatidagi tartibga asoslangan bo‘lib, ulamolar uning sanadi va ismlar ro‘yxati haqida turlicha fikr bildirgan, ' +
      'shuning uchun bu mashhur ro‘yxat sifatida beriladi. ' +
      'Ma’nolar qisqa mazmuniy tarjima. Hadis raqamlarini sunnah.com da tekshirib ko‘ring.</div></div>';

    el.innerHTML = h;
    renderList();
  }

  /* ---------- HODISALAR ---------- */
  function onClick(e) {
    var b = e.target.closest('[data-a]');
    if (!b) return;
    var a = b.getAttribute('data-a');
    if (a === 'tab') {
      S.tab = b.getAttribute('data-t');
      T.$$('.tabs .tab', el).forEach(function (x) {
        x.classList.toggle('active', x.getAttribute('data-t') === S.tab);
      });
      renderList();
    } else if (a === 'fav') {
      var n = +b.getAttribute('data-n');
      var on = toggleFav(n);
      T.tg.haptic('light');
      if (S.tab === 'fav' && !on) renderList();
      else {
        b.textContent = on ? '★' : '☆';
        b.classList.toggle('on', on);
        var ft = $('nmFavTab');
        if (ft) ft.textContent = '★ Sevimlilar (' + favs().length + ')';
      }
      T.toast(on ? 'Sevimlilarga qo‘shildi' : 'Sevimlilardan olindi');
    } else if (a === 'share') {
      var d = N[+b.getAttribute('data-n') - 1];
      T.tg.share(d[0] + '\n' + d[1] + ' — ' + d[2] + '\n(' + b.getAttribute('data-n') + '/99)');
    }
  }

  T.sections.names = {
    title: 'Allohning 99 go‘zal ismi',
    icon: '✨',
    render: function (root) {
      el = root;
      S.q = '';
      el.onclick = onClick;
      el.oninput = function (e) {
        if (e.target.id === 'nmSearch') { S.q = e.target.value; renderList(); }
      };
      renderAll();
    },
    leave: function () {
      if (el) { el.onclick = null; el.oninput = null; }
      el = null;
    }
  };
})();
