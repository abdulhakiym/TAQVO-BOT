/* TAQVO PRO MAX — Tonggi / kechki zikr: bittadan zikr, sanagich, keyingisiga avtomatik o'tish, ro'yxat.
   Ma'lumotlar: js/zikr-data.js */
(() => {
  const tg = window.Telegram && window.Telegram.WebApp;
  const TITLES = { morning: 'Tonggi zikr', evening: 'Kechki zikr' };
  const CIRC = 2 * Math.PI * 54;
  const day = () => new Date().toLocaleDateString('en-CA');
  const read = (k) => { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } };
  const write = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const buzz = (type) => { try { if (tg && tg.HapticFeedback) { type === 'ok' ? tg.HapticFeedback.notificationOccurred('success') : tg.HapticFeedback.impactOccurred('light'); } } catch (e) {} };

  function el(tag, cls, text) {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  const svg = (tag, attrs) => {
    const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  };

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

  let timer = null;

  function render(kind, root) {
    clearTimeout(timer);
    const items = window.ZIKR_DATA[kind];
    const key = 'z2:' + kind + ':' + day();
    const counts = read(key);
    const done = (i) => (counts[i.id] || 0) >= i.n;
    let idx = Math.max(0, items.findIndex((i) => !done(i)));
    let showList = false;

    function paint() {
      clearTimeout(timer);
      root.textContent = '';
      const finished = items.every(done);
      const doneCount = items.filter(done).length;

      // yuqori chiziq: 14 ta bo'lak
      const top = el('div', 'zk-top');
      top.appendChild(el('span', 'zk-pos', finished ? 'Hammasi bajarildi' : 'Zikr ' + (idx + 1) + ' / ' + items.length));
      const listBtn = el('button', 'zk-chip', showList ? 'Zikrga qaytish' : 'Ro‘yxat');
      listBtn.onclick = () => { showList = !showList; paint(); };
      top.appendChild(listBtn);
      root.appendChild(top);

      const segs = el('div', 'zk-segs');
      items.forEach((it, i) => {
        const s = el('i', done(it) ? 'on' : (i === idx ? 'cur' : ''));
        segs.appendChild(s);
      });
      root.appendChild(segs);

      if (showList) return paintList(doneCount);
      if (finished) return paintFinish();
      paintCard();
    }

    function paintList(doneCount) {
      root.appendChild(el('p', 'zk-note', doneCount + ' / ' + items.length + ' zikr bajarildi'));
      items.forEach((it, i) => {
        const row = el('button', 'zk-row' + (done(it) ? ' ok' : ''));
        row.appendChild(el('b', null, (i + 1) + '. ' + it.t));
        row.appendChild(el('span', null, done(it) ? '✓ ' + it.n + ' / ' + it.n : (counts[it.id] || 0) + ' / ' + it.n));
        row.onclick = () => { idx = i; showList = false; paint(); };
        root.appendChild(row);
      });
      const reset = el('button', 'zk-reset', 'Bugungi hisobni boshidan boshlash');
      reset.onclick = () => { Object.keys(counts).forEach((k) => delete counts[k]); write(key, counts); idx = 0; showList = false; paint(); };
      root.appendChild(reset);
    }

    function paintFinish() {
      const box = el('div', 'zk-finish');
      box.appendChild(el('h3', null, 'Alloh qabul qilsin'));
      box.appendChild(el('p', null, TITLES[kind] + ' to‘liq bajarildi. Bu sunnatni davom ettiring, Alloh sizga ham, bizga ham ajr bersin.'));
      const again = el('button', 'zk-btn', 'Qaytadan boshlash');
      again.onclick = () => { Object.keys(counts).forEach((k) => delete counts[k]); write(key, counts); idx = 0; paint(); };
      const list = el('button', 'zk-chip', 'Ro‘yxatni ko‘rish');
      list.onclick = () => { showList = true; paint(); };
      box.appendChild(again); box.appendChild(list);
      root.appendChild(box);
    }

    function paintCard() {
      const it = items[idx];
      const card = el('div', 'zk-card');
      card.appendChild(el('h3', null, it.t));

      const ar = el('p', 'zk-ar', it.ar || ''); ar.setAttribute('dir', 'rtl'); ar.lang = 'ar';
      card.appendChild(ar);
      const tr = el('p', 'zk-tr', it.tr || '');
      const uz = el('p', 'zk-uz', it.uz || '');
      if (it.tr) card.appendChild(tr);
      card.appendChild(uz);
      if (it.q) {
        ar.textContent = 'Yuklanmoqda…';
        quran(it.q).then((v) => { ar.textContent = v.ar; uz.textContent = v.uz; })
          .catch(() => { ar.textContent = ''; uz.textContent = 'Matnni yuklab bo‘lmadi. Internetni tekshirib, qayta oching.'; });
      }
      const fz = el('div', 'zk-fazl');
      fz.appendChild(el('b', null, 'Fazilati'));
      fz.appendChild(el('p', null, it.fazl));
      card.appendChild(fz);
      card.appendChild(el('p', 'zk-src', 'Manba: ' + it.src));
      root.appendChild(card);

      // sanagich: halqa
      const wrap = el('div', 'zk-counter');
      const btn = el('button', 'zk-ring'); btn.setAttribute('aria-label', 'Sanash');
      const s = svg('svg', { viewBox: '0 0 120 120' });
      s.appendChild(svg('circle', { cx: 60, cy: 60, r: 54, class: 'bg' }));
      const prog = svg('circle', { cx: 60, cy: 60, r: 54, class: 'fg', 'stroke-dasharray': CIRC });
      s.appendChild(prog);
      btn.appendChild(s);
      const num = el('span', 'zk-num');
      btn.appendChild(num);
      wrap.appendChild(btn);
      wrap.appendChild(el('p', 'zk-hint', it.n > 1 ? 'Hadisda ' + it.n + ' marta kelgan. Har o‘qiganda bosing.' : 'O‘qib bo‘lgach bosing.'));
      root.appendChild(wrap);

      const upd = () => {
        const c = Math.min(counts[it.id] || 0, it.n);
        num.textContent = c + ' / ' + it.n;
        prog.setAttribute('stroke-dashoffset', CIRC * (1 - c / it.n));
        wrap.classList.toggle('full', c >= it.n);
      };
      upd();

      btn.onclick = () => {
        const c = counts[it.id] || 0;
        if (c >= it.n) return;
        counts[it.id] = c + 1; write(key, counts);
        upd();
        if (counts[it.id] >= it.n) {
          buzz('ok');
          // keyingi tugallanmagan zikrga avtomatik o'tish
          timer = setTimeout(() => {
            const nxt = items.findIndex((x, i) => i > idx && !done(x));
            const any = items.findIndex((x) => !done(x));
            idx = nxt !== -1 ? nxt : (any !== -1 ? any : idx);
            paint(); window.scrollTo(0, 0);
          }, 650);
        } else buzz();
      };

      const nav = el('div', 'zk-nav');
      const prev = el('button', 'zk-chip', '‹ Oldingi');
      const next = el('button', 'zk-chip', 'Keyingi ›');
      prev.disabled = idx === 0; next.disabled = idx === items.length - 1;
      prev.onclick = () => { idx--; paint(); window.scrollTo(0, 0); };
      next.onclick = () => { idx++; paint(); window.scrollTo(0, 0); };
      nav.appendChild(prev); nav.appendChild(next);
      root.appendChild(nav);
    }

    paint();
    return { title: TITLES[kind], status: items.length + ' ta zikr' };
  }

  window.TaqvoZikr = { render };
})();
