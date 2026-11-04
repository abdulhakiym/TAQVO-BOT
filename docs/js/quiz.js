/* TAQVO PRO MAX — Islomiy bilim, Viktorina, TAQVO AI, Islomiy media, Reyting.
   Viktorina hozircha telefonda hisoblanadi; server tomonidagi hisob va umumiy reyting backend bilan keyingi qadamda. */
(() => {
  const tg = window.Telegram && window.Telegram.WebApp;
  const el = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; };
  const get = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const put = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const buzz = (ok) => { try { if (tg && tg.HapticFeedback) { ok ? tg.HapticFeedback.notificationOccurred('success') : tg.HapticFeedback.notificationOccurred('error'); } } catch (e) {} };
  const card = (h, lines, src) => { const c = el('div', 'zk-card'); c.style.marginBottom = '10px'; c.appendChild(el('h3', null, h));
    lines.forEach((l) => c.appendChild(el('p', 'zk-uz', l))); if (src) c.appendChild(el('p', 'zk-src', 'Manba: ' + src)); return c; };
  const NOTE = 'Bu umumiy ta’limiy ma’lumot, fatvo emas. Murakkab masalalarda ishonchli olimga murojaat qiling.';

  // ---------------- ISLOMIY BILIM
  const KB = {
    'Aqida': [['Tavhid', ['Alloh yagona, Uning sherigi yo‘q. Ibodat faqat Allohga qilinadi.'], 'Qur’on 112:1-4'], ['Shirk', ['Allohga sherik keltirish eng katta gunoh. Alloh shirkni, tavba qilinmasa, kechirmaydi.'], 'Qur’on 4:48'], ['Payg‘ambarlar', ['Alloh insonlarga to‘g‘ri yo‘lni ko‘rsatish uchun payg‘ambarlar yuborgan. Muhammad ﷺ oxirgi payg‘ambardir.'], 'Qur’on 33:40']],
    'Ibodat': [['Ibodatning maqsadi', ['Alloh jin va insonni faqat Unga ibodat qilishlari uchun yaratgan.'], 'Qur’on 51:56'], ['Ibodat turlari', ['Namoz, ro‘za, zakot, haj, duo, zikr va Qur’on tilovati. Batafsil “Farz amallar” va “Fiqh” bo‘limlarida.'], '']],
    'Axloq': [['Ota-onaga yaxshilik', ['Alloh Unga ibodat qilishni va ota-onaga yaxshilik qilishni buyurgan.'], 'Qur’on 17:23'], ['Qo‘shni haqqi', ['Ota-onaga, qarindoshlarga, yetimlarga va qo‘shnilarga yaxshilik qilish buyurilgan.'], 'Qur’on 4:36'], ['G‘iybat va masxara', ['Birovning orqasidan gapirish va bir-birini kamsitishdan qaytarilgan.'], 'Qur’on 49:11-12'], ['Yaxshi so‘z', ['Kim Allohga va oxirat kuniga iymon keltirgan bo‘lsa, yaxshi gapirsin yoki sukut qilsin.'], 'Buxoriy 6018, Muslim 47']],
    'Islom tarixi': [['Xulafoi roshidin', ['Abu Bakr (11-13 hijriy), Umar (13-23), Usmon (23-35), Ali (35-40) roziyallohu anhum.'], 'Tarix kitoblari'], ['Keyingi davlatlar', ['Umaviylar (661-750), Abbosiylar (750-1258).'], 'Tarix kitoblari']],
    'Asosiy bilim': [['Hijriy oylar', ['Muharram, Safar, Rabi’ul-avval, Rabi’ul-oxir, Jumodul-avval, Jumodul-oxir, Rajab, Sha’bon, Ramazon, Shavvol, Zul-qa’da, Zul-hijja.'], ''], ['Harom oylar', ['Zul-qa’da, Zul-hijja, Muharram va Rajab.'], 'Qur’on 9:36; Buxoriy 3197'], ['Hayitlar', ['Ro‘za hayit (1-shavvol) va Qurbon hayit (10-zul-hijja).'], 'Buxoriy, Muslim']],
  };
  function knowledge(root, cur) {
    root.textContent = ''; cur = cur || 'Aqida';
    const tabs = el('div', 'q-tabs'); Object.keys(KB).forEach((k) => { const b = el('button', 'zk-chip' + (k === cur ? ' act' : ''), k); b.onclick = () => knowledge(root, k); tabs.appendChild(b); });
    root.appendChild(tabs); KB[cur].forEach((i) => root.appendChild(card(i[0], i[1], i[2]))); root.appendChild(el('p', 'zk-src', NOTE));
    return { title: 'Islomiy bilim', status: Object.keys(KB).length + ' ta yo‘nalish' };
  }

  // ---------------- VIKTORINA
  const QS = [
    ['Islomning nechta ustuni bor?', ['3', '5', '6', '7'], 'Islom besh ustun ustiga qurilgan (Buxoriy 8, Muslim 16).'],
    ['Qur’onda nechta sura bor?', ['99', '110', '114', '120'], 'Qur’on 114 suradan iborat.'],
    ['Qur’onning birinchi surasi qaysi?', ['Baqara', 'Fotiha', 'Ixlos', 'Nos'], 'Birinchi sura Fotiha.'],
    ['Qur’onning eng uzun surasi qaysi?', ['Oli Imron', 'Niso', 'Baqara', 'Moida'], 'Eng uzun sura Baqara (286 oyat).'],
    ['Ramazon hijriy yilning nechanchi oyi?', ['7-oy', '8-oy', '9-oy', '10-oy'], 'Ramazon to‘qqizinchi oy.'],
    ['Kuniga necha vaqt namoz farz?', ['3', '4', '5', '6'], 'Kuniga besh vaqt namoz farz.'],
    ['Payg‘ambarimiz ﷺ qaysi shaharda tug‘ilgan?', ['Madina', 'Makka', 'Toif', 'Quddus'], 'Makkada tug‘ilganlar.'],
    ['Hijrat qaysi shaharga qilingan?', ['Habashiston', 'Toif', 'Madina', 'Quddus'], 'Rasululloh ﷺ Madinaga hijrat qildilar.'],
    ['Birinchi vahiy qaysi g‘orda tushgan?', ['Savr', 'Hiro', 'Uhud', 'Arqam'], 'Birinchi vahiy Hiro g‘orida tushgan.'],
    ['Payg‘ambarimiz ﷺ necha yoshda vafot etdilar?', ['60', '61', '63', '65'], '63 yoshda vafot etdilar.'],
    ['Ixlos surasi Qur’onda nechanchi?', ['110', '112', '113', '114'], 'Ixlos surasi 112-sura.'],
    ['Zakot nisobga yetgan molning necha foizi?', ['1%', '2,5%', '5%', '10%'], 'Zakot 2,5 foiz.'],
    ['Badr g‘azoti qaysi oyda bo‘lgan?', ['Ramazon', 'Rajab', 'Muharram', 'Shavvol'], 'Badr g‘azoti Ramazon oyida bo‘ldi.'],
    ['Besh vaqt namoz qaysi hodisada farz qilingan?', ['Hijrat', 'Me’roj', 'Badr', 'Makka fathi'], 'Namoz Me’roj kechasi farz bo‘lgan.'],
    ['Iymonning nechta rukni bor?', ['4', '5', '6', '7'], 'Iymon oltita asosga ega (Muslim 8).'],
    ['Payg‘ambarimizning ﷺ birinchi turmush o‘rtog‘i kim?', ['Oisha', 'Xadicha', 'Hafsa', 'Zaynab'], 'Xadicha roziyallohu anho.'],
    ['Birinchi muazzin kim bo‘lgan?', ['Bilol', 'Abu Bakr', 'Umar', 'Ali'], 'Birinchi muazzin Bilol roziyallohu anhu.'],
    ['Madinada qurilgan birinchi masjid qaysi?', ['Quba', 'Qiblatayn', 'Nabaviy', 'Ijoba'], 'Quba masjidi Islomning birinchi masjidi sifatida Madina yaqinida qurilgan.'],
    ['Qur’onning eng qisqa surasi qaysi?', ['Ixlos', 'Asr', 'Kavsar', 'Nos'], 'Kavsar surasi 3 oyatdan iborat.'],
    ['Ramazon ro‘zasi qaysi hijriy yilda farz qilingan?', ['1-yil', '2-yil', '5-yil', '8-yil'], 'Ro‘za 2-hijriy yilda farz qilingan.'],
    ['Hanafiy mazhabida vitr namozi qanday hukmda?', ['Sunnat', 'Vojib', 'Nafl', 'Mustahab'], 'Hanafiyda vitr vojib.'],
    ['Qurbon hayit qaysi sanada?', ['1-shavvol', '10-zul-hijja', '1-muharram', '15-sha’bon'], 'Qurbon hayit 10-zul-hijjada.'],
  ];
  const ST = () => Object.assign({ pts: 0, rounds: 0, ok: 0, all: 0 }, get('quiz:stats', {}));
  function quiz(root) {
    root.textContent = '';
    const s = ST();
    const box = card('Bilimingizni sinang', ['Har bir to‘g‘ri javob uchun +20 ball. Raund tugasa +10, hammasi to‘g‘ri bo‘lsa +30 ball qo‘shimcha. Hisob serverda yuritiladi.'], '');
    box.appendChild(el('p', 'zk-uz', 'Ballaringiz: ' + s.pts + '  ·  Raundlar: ' + s.rounds));
    const go = el('button', 'zk-btn', 'Raundni boshlash (5 savol)'); go.style.marginTop = '12px'; go.onclick = () => round(root);
    box.appendChild(go); root.appendChild(box);
    return { title: 'Viktorina', status: QS.length + ' ta savol' };
  }
  const api = (p, b) => window.TaqvoApi.post(p, b);
  const fail = (root, e, back) => { root.textContent = ''; root.appendChild(el('div', 'empty', e.message || 'Server bilan ulanib bo‘lmadi. Birozdan keyin urinib ko‘ring.'));
    const b = el('button', 'zk-chip', 'Orqaga'); b.onclick = back; root.appendChild(b); };
  async function round(root) {
    root.textContent = ''; root.appendChild(el('p', 'zk-note', 'Yuklanmoqda…'));
    let R; try { R = await api('/api/quiz/start'); } catch (e) { return fail(root, e, () => quiz(root)); }
    let i = 0;
    const show = async () => {
      root.textContent = '';
      if (i >= R.qids.length) {
        let f; try { f = await api('/api/quiz/finish', { round: R.round }); } catch (e) { return fail(root, e, () => quiz(root)); }
        const s = ST(); s.pts = f.total; s.rounds++; s.ok += f.right; s.all += R.qids.length; put('quiz:stats', s);
        const c = el('div', 'zk-finish'); c.appendChild(el('h3', null, f.right + ' / ' + R.qids.length));
        c.appendChild(el('p', null, '+' + f.gain + ' ball. Jami: ' + f.total));
        const a = el('button', 'zk-btn', 'Yana o‘ynash'); a.onclick = () => round(root); const b = el('button', 'zk-chip', 'Orqaga'); b.onclick = () => quiz(root);
        c.appendChild(a); c.appendChild(b); root.appendChild(c); return;
      }
      const q = QS[R.qids[i]]; root.appendChild(el('p', 'zk-note', 'Savol ' + (i + 1) + ' / ' + R.qids.length));
      const c = el('div', 'zk-card'); c.appendChild(el('h3', null, q[0])); root.appendChild(c);
      const info = el('p', 'zk-uz'); let busy = false;
      q[1].forEach((o, k) => { const b = el('button', 'zk-row', o); b.style.marginTop = '8px';
        b.onclick = async () => { if (busy) return; busy = true; let r;
          try { r = await api('/api/quiz/answer', { round: R.round, qid: R.qids[i], a: k }); } catch (e) { busy = false; return fail(root, e, () => quiz(root)); }
          buzz(r.ok); b.classList.add(r.ok ? 'good' : 'bad'); if (!r.ok) c.querySelectorAll('.zk-row')[r.correct].classList.add('good');
          info.textContent = (r.ok ? 'To‘g‘ri. ' : 'Noto‘g‘ri. ') + q[2]; const n = el('button', 'zk-btn', i + 1 < R.qids.length ? 'Keyingisi' : 'Natija'); n.style.marginTop = '12px';
          n.onclick = () => { i++; show(); }; c.appendChild(info); c.appendChild(n); };
        c.appendChild(b); });
    };
    show();
  }

  // ---------------- AI, MEDIA, REYTING
  function ai(root) {
    root.textContent = '';
    root.appendChild(card('TAQVO AI', ['Islomiy savollaringizga o‘zbek tilida javob beradi. Murakkab fatvo masalalarida olimga murojaat qilishni tavsiya qiladi va manba to‘qimaydi.', 'Savolingizni botga yozing: pastdagi tugma ilovani yopib, suhbatga qaytaradi.'], ''));
    const b = el('button', 'zk-btn', 'Botga o‘tish va savol yozish'); b.onclick = () => { if (tg) tg.close(); }; root.appendChild(b);
    return { title: 'TAQVO AI', status: 'Bot orqali ishlaydi' };
  }
  function media(root) {
    root.textContent = '';
    root.appendChild(card('Islomiy media', ['Foydali eslatmalar, ta’limiy videolar va yangiliklar rasmiy kanalimizda e’lon qilinadi.'], '@hakiymqalb'));
    const b = el('button', 'zk-btn', 'Kanalga o‘tish'); b.onclick = () => { const u = 'https://t.me/hakiymqalb'; if (tg && tg.openTelegramLink) tg.openTelegramLink(u); else window.open(u, '_blank'); };
    root.appendChild(b);
    return { title: 'Islomiy media', status: 'Kanal' };
  }
  async function leaderboard(root, per) {
    root.textContent = ''; per = per || 'day';
    const L = { day: 'Kunlik', week: 'Haftalik', month: 'Oylik', all: 'Umumiy' };
    const tabs = el('div', 'q-tabs'); Object.keys(L).forEach((k) => { const b = el('button', 'zk-chip' + (k === per ? ' act' : ''), L[k]); b.onclick = () => leaderboard(root, k); tabs.appendChild(b); });
    root.appendChild(tabs); const box = el('div'); root.appendChild(box); box.appendChild(el('p', 'zk-note', 'Yuklanmoqda…'));
    try {
      const d = await window.TaqvoApi.get('/api/leaderboard?period=' + per); box.textContent = '';
      if (!d.top.length) box.appendChild(el('div', 'empty', 'Hali natija yo‘q. Viktorinada birinchi bo‘ling!'));
      d.top.forEach((u, i) => { const r = el('div', 'zk-row' + (u.me ? ' ok' : '')); r.appendChild(el('b', null, ['🥇', '🥈', '🥉'][i] || (i + 1) + '.')); r.lastChild.style.marginRight = '8px';
        const nm = el('b', null, u.name); nm.style.flex = '1'; r.appendChild(nm); r.appendChild(el('span', null, u.pts + ' ball')); box.appendChild(r); });
      box.appendChild(el('p', 'zk-note', 'Sizning o‘rningiz: ' + (d.me.pts ? d.me.rank + '-o‘rin, ' + d.me.pts + ' ball' : 'hali natija yo‘q')));
      const nb = el('button', 'zk-reset', 'Reytingdagi ismimni o‘zgartirish');
      nb.onclick = async () => { const v = prompt('Reytingda ko‘rinadigan ism (2-24 belgi)', ''); if (!v) return;
        try { await window.TaqvoApi.post('/api/profile/name', { name: v }); leaderboard(root, per); } catch (e) { alert(e.message); } };
      box.appendChild(nb);
    } catch (e) { box.textContent = ''; box.appendChild(el('div', 'empty', e.message || 'Reytingni yuklab bo‘lmadi.')); }
    return { title: 'Reyting', status: L[per] };
  }

  window.TaqvoSections = window.TaqvoSections || {};
  Object.assign(window.TaqvoSections, { knowledge, quiz, ai, media, leaderboard });
})();
