/* TAQVO PRO MAX — Tonggi va kechki zikr.
   Manbalar: faqat Buxoriy va Muslim hadislari; Qur'on matni (arabcha + o'zbekcha) alquran.cloud API'dan olinadi.
   Hadis raqamlarini nashrdan oldin sunnah.com'da tekshiring. */
(() => {
  const SAHIH = 'Faqat Buxoriy va Muslim hadislaridan olingan zikrlar.';
  const ISTIGFOR = 'اللَّهُمَّ أَنْتَ رَبِّي لَا إِلَهَ إِلَّا أَنْتَ، خَلَقْتَنِي وَأَنَا عَبْدُكَ، وَأَنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ، أَعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ، أَبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ، وَأَبُوءُ بِذَنْبِي فَاغْفِرْ لِي فَإِنَّهُ لَا يَغْفِرُ الذُّنُوبَ إِلَّا أَنْتَ';

  const COMMON = [
    { id: 'tasbeh100', t: 'Tasbeh', ar: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ', uz: 'Kim kuniga yuz marta shuni aytsa, gunohlari dengiz ko‘pigicha bo‘lsa ham kechiriladi.', n: 100, src: 'Buxoriy 6405, Muslim 2691' },
    { id: 'tahlil100', t: 'Tahlil', ar: 'لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ', uz: 'Kuniga yuz marta aytgan kishi o‘nta qul ozod qilgan savobini oladi, yuzta yaxshilik yoziladi, yuzta yomonlik o‘chiriladi va kun bo‘yi shaytondan himoyada bo‘ladi.', n: 100, src: 'Buxoriy 3293, Muslim 2691' },
    { id: 'azim', t: 'Ikki yengil kalima', ar: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ', uz: 'Tilga yengil, mezonda og‘ir, Rahmonga suyukli ikki kalima. Soni belgilanmagan, 33 marta tavsiya qilamiz.', n: 33, src: 'Buxoriy 6406, Muslim 2694' },
    { id: 'istigfor', t: 'Istig‘for', ar: 'أَسْتَغْفِرُ اللَّهَ وَأَتُوبُ إِلَيْهِ', uz: 'Rasululloh ﷺ kuniga yuz marta tavba qilganlar. Alloh sendan mag‘firat so‘rashingni yoqtiradi.', n: 100, src: 'Muslim 2702, Buxoriy 6307' },
    { id: 'hawqala', t: 'Hawqala', ar: 'لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ', uz: 'Jannat xazinalaridan bir xazinadir.', n: 10, src: 'Buxoriy 6384, Muslim 2704' },
    { id: 'salovat', t: 'Salovat', ar: 'اللَّهُمَّ صَلِّ عَلَى مُحَمَّدٍ', uz: 'Kim Payg‘ambarimizga ﷺ bir marta salovat aytsa, Alloh unga o‘n marta salovat aytadi.', n: 10, src: 'Muslim 408' },
  ];
  const SAYYID = (when) => ({ id: 'sayyid', t: 'Sayyidul istig‘for', ar: ISTIGFOR, uz: 'Kim uni ' + when + ' ishonch bilan aytsa va o‘sha ' + (when === 'ertalab' ? 'kun' : 'kecha') + ' vafot etsa, jannat ahlidan bo‘ladi.', n: 1, src: 'Buxoriy 6306' });
  const ASBAH = (a) => ({ id: 'mulk', t: a ? 'Tonggi duo' : 'Kechki duo', ar: a ? 'أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ' : 'أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ وَالْحَمْدُ لِلَّهِ لَا إِلَهَ إِلَّا اللَّهُ وَحْدَهُ لَا شَرِيكَ لَهُ', uz: (a ? 'Tong otdi' : 'Kech kirdi') + ' va mulk Allohnikidir, hamd Allohgadir. Allohdan o‘zga iloh yo‘q, U yagona, sherigi yo‘q. (Duoning davomi bor, to‘liq matn Muslim kitobida.)', n: 1, src: 'Muslim 2723' });

  const KINDS = {
    morning: { title: 'Tonggi zikr', items: [SAYYID('ertalab'), ASBAH(true), ...COMMON] },
    evening: {
      title: 'Kechki zikr',
      items: [
        { id: 'kursi', t: 'Oyatul Kursi', q: '2:255', n: 1, src: 'Qur’on 2:255. Uyquga yotganda o‘qigan kishiga Alloh tomonidan himoyachi bo‘lishi haqida: Buxoriy 2311' },
        { id: 'ikhlos', t: 'Ixlos surasi', q: 's112', n: 3, src: 'Qur’on 112. Buxoriy 5017: uyqu oldidan Ixlos, Falaq, Nos o‘qilib tanaga surtilgan' },
        { id: 'falaq', t: 'Falaq surasi', q: 's113', n: 3, src: 'Qur’on 113. Buxoriy 5017' },
        { id: 'nos', t: 'Nos surasi', q: 's114', n: 3, src: 'Qur’on 114. Buxoriy 5017' },
        SAYYID('kechqurun'), ASBAH(false), ...COMMON,
      ],
    },
  };

  const today = () => new Date().toLocaleDateString('en-CA');
  const load = (k) => { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } };
  const save = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const tg = window.Telegram && window.Telegram.WebApp;

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  async function quran(ref) {
    const ck = 'qa:' + ref;
    try { const c = localStorage.getItem(ck); if (c) return JSON.parse(c); } catch (e) {}
    const surah = ref.charAt(0) === 's';
    const r = await fetch('https://api.alquran.cloud/v1/' + (surah ? 'surah/' + ref.slice(1) : 'ayah/' + ref) + '/editions/quran-uthmani,uz.sodik');
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const d = (await r.json()).data;
    const join = (e) => (surah ? e.ayahs.map((a) => a.text).join(' ') : e.text);
    const out = { ar: join(d[0]), uz: join(d[1]) };
    try { localStorage.setItem(ck, JSON.stringify(out)); } catch (e) {}
    return out;
  }

  function render(kind, root) {
    const K = KINDS[kind];
    const key = 'z:' + kind + ':' + today();
    const state = load(key);
    root.textContent = '';

    const banner = el('div', 'zbanner');
    banner.appendChild(el('b', null, 'Sunnatni tiriltiring'));
    banner.appendChild(el('p', null, 'Rabbini zikr qilgan kishi bilan zikr qilmagan kishining o‘xshashi tirik va o‘lik kabidir. (Buxoriy 6407)'));
    const bar = el('div', 'zbar'); const fill = el('i'); bar.appendChild(fill);
    const prog = el('p', 'zprog');
    banner.appendChild(bar); banner.appendChild(prog);
    root.appendChild(banner);

    const refresh = () => {
      const done = K.items.filter((i) => (state[i.id] || 0) >= i.n).length;
      fill.style.width = Math.round((done / K.items.length) * 100) + '%';
      prog.textContent = done + ' / ' + K.items.length + ' zikr bajarildi';
    };

    K.items.forEach((it) => {
      const card = el('div', 'zcard');
      card.appendChild(el('h3', null, it.t));
      const ar = el('p', 'zar', it.ar || ''); ar.setAttribute('dir', 'rtl'); ar.lang = 'ar';
      const uz = el('p', 'zuz', it.uz || '');
      if (it.q) {
        ar.textContent = 'Yuklanmoqda…';
        quran(it.q).then((v) => { ar.textContent = v.ar; uz.textContent = v.uz; })
          .catch(() => { ar.textContent = ''; uz.textContent = 'Matnni yuklab bo‘lmadi. Internetni tekshirib, qayta oching.'; });
      }
      card.appendChild(ar); card.appendChild(uz);
      card.appendChild(el('p', 'zsrc', 'Manba: ' + it.src));

      const btn = el('button', 'zcnt');
      const paint = () => {
        const c = state[it.id] || 0;
        btn.textContent = c >= it.n ? '✓ Bajarildi (' + it.n + ')' : c + ' / ' + it.n + '  ·  bosing';
        card.classList.toggle('done', c >= it.n);
      };
      btn.onclick = () => {
        const c = state[it.id] || 0;
        if (c >= it.n) return;
        state[it.id] = c + 1; save(key, state);
        if (tg && tg.HapticFeedback) { try { tg.HapticFeedback.impactOccurred('light'); } catch (e) {} }
        paint(); refresh();
      };
      paint();
      card.appendChild(btn);
      root.appendChild(card);
    });

    const reset = el('button', 'zreset', 'Bugungi hisobni boshidan boshlash');
    reset.onclick = () => { save(key, {}); render(kind, root); };
    root.appendChild(reset);
    root.appendChild(el('p', 'zsrc', SAHIH));
    refresh();
    return { title: K.title, status: 'Ishlaydi' };
  }

  window.TaqvoZikr = { render };
})();
