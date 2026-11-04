/* TAQVO PRO MAX — Qur'on: suralar, juzlar, belgilar, oxirgi o'qilgan, audio. Matn va tarjima: alquran.cloud (o'zgartirilmaydi). */
(() => {
  const API = 'https://api.alquran.cloud/v1/', ED = '/editions/quran-uthmani,uz.sodik';
  const get = (k, d) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } };
  const put = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };
  const el = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; };
  const jget = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error(r.status); return (await r.json()).data; };
  let audio = null;
  const stop = () => { if (audio) { audio.pause(); audio = null; } };

  async function surahs() {
    const c = get('q:surahs', null); if (c) return c;
    const d = (await jget(API + 'surah')).map((s) => ({ n: s.number, ar: s.name, en: s.englishName, c: s.numberOfAyahs }));
    put('q:surahs', d); return d;
  }

  function render(root, tab) {
    stop(); root.textContent = '';
    tab = tab || 'surah';
    const tabs = el('div', 'q-tabs');
    [['surah', 'Suralar'], ['juz', 'Juzlar'], ['bm', 'Belgilar']].forEach(([k, t]) => {
      const b = el('button', 'zk-chip' + (k === tab ? ' act' : ''), t); b.onclick = () => render(root, k); tabs.appendChild(b);
    });
    root.appendChild(tabs);
    const last = get('q:last', null);
    if (last && tab !== 'bm') {
      const b = el('button', 'q-last', '📍 Oxirgi o‘qilgan: ' + last.label + (last.a ? ', ' + last.a + '-oyat' : ''));
      b.onclick = () => reader(root, last.t, last.n, last.a); root.appendChild(b);
    }
    const body = el('div'); root.appendChild(body);
    if (tab === 'juz') {
      const g = el('div', 'q-grid');
      for (let i = 1; i <= 30; i++) { const b = el('button', 'q-juz', i + '-juz'); b.onclick = () => reader(root, 'j', i); g.appendChild(b); }
      body.appendChild(g);
    } else if (tab === 'bm') {
      const bm = get('q:bm', []);
      if (!bm.length) body.appendChild(el('div', 'empty', 'Hali belgi qo‘yilmagan. O‘qiyotganda oyatdagi ★ tugmasini bosing.'));
      bm.forEach((b) => { const r = el('button', 'zk-row', b.label + ', ' + b.a + '-oyat'); r.onclick = () => reader(root, 's', b.s, b.a); body.appendChild(r); });
    } else {
      const q = el('input', 'q-search'); q.type = 'search'; q.placeholder = 'Sura qidirish (nomi yoki raqami)';
      const box = el('div'); body.appendChild(q); body.appendChild(box);
      box.appendChild(el('p', 'zk-note', 'Yuklanmoqda…'));
      surahs().then((all) => {
        const draw = () => {
          const t = q.value.trim().toLowerCase(); box.textContent = '';
          all.filter((s) => !t || String(s.n) === t || s.en.toLowerCase().includes(t) || s.ar.includes(t)).forEach((s) => {
            const r = el('button', 'zk-row'); r.appendChild(el('b', null, s.n + '. ' + s.en)); r.appendChild(el('span', 'q-arn', s.ar + '  ·  ' + s.c));
            r.onclick = () => reader(root, 's', s.n); box.appendChild(r);
          });
        };
        q.oninput = draw; draw();
      }).catch(() => { box.textContent = ''; box.appendChild(el('div', 'empty', 'Suralar ro‘yxatini yuklab bo‘lmadi. Internetni tekshiring.')); });
    }
  }

  async function reader(root, t, n, focus) {
    stop(); root.textContent = '';
    const back = el('button', 'zk-chip', '‹ Ro‘yxat'); back.onclick = () => render(root, t === 'j' ? 'juz' : 'surah');
    root.appendChild(back);
    const note = el('p', 'zk-note', 'Yuklanmoqda…'); root.appendChild(note);
    let items;
    try {
      const d = await jget(API + (t === 'j' ? 'juz/' : 'surah/') + n + ED);
      items = d[0].ayahs.map((a, i) => ({ ar: a.text, uz: d[1].ayahs[i].text, g: a.number, n: a.numberInSurah,
        s: t === 'j' ? a.surah.number : d.length && d[0].number, sn: t === 'j' ? a.surah.englishName : d[0].englishName }));
    } catch (e) { note.textContent = ''; root.appendChild(el('div', 'empty', 'Matnni yuklab bo‘lmadi. Internetni tekshirib, qayta urinib ko‘ring.')); return; }
    note.remove();
    const title = t === 'j' ? n + '-juz' : items[0].sn;
    const bar = el('div', 'q-bar'); bar.appendChild(el('b', null, title));
    const play = el('button', 'zk-chip', '▶ Tinglash'); bar.appendChild(play); root.appendChild(bar);
    const cards = []; let bm = get('q:bm', []);
    items.forEach((it, i) => {
      if (it.n === 1) root.appendChild(el('h3', 'q-sura', it.sn));
      const c = el('div', 'q-ayah'); cards.push(c);
      const ar = el('p', 'q-ar', it.ar); ar.dir = 'rtl'; ar.lang = 'ar'; c.appendChild(ar);
      c.appendChild(el('p', 'zk-uz', it.uz));
      const f = el('div', 'q-foot'); f.appendChild(el('span', null, it.sn + ' ' + it.s + ':' + it.n));
      const key = it.s + ':' + it.n, label = it.sn + ' ' + it.s;
      const star = el('button', 'q-ic', bm.some((b) => b.k === key) ? '★' : '☆');
      star.onclick = () => { bm = get('q:bm', []); const x = bm.findIndex((b) => b.k === key);
        if (x >= 0) bm.splice(x, 1); else bm.push({ k: key, s: it.s, a: it.n, label: it.sn }); put('q:bm', bm); star.textContent = x >= 0 ? '☆' : '★'; };
      const pin = el('button', 'q-ic', '📍'); pin.onclick = () => { put('q:last', { t, n, a: it.n, label: title }); pin.textContent = '✓'; };
      const pl = el('button', 'q-ic', '▶'); pl.onclick = () => go(i);
      f.appendChild(pl); f.appendChild(star); f.appendChild(pin); c.appendChild(f); root.appendChild(c);
    });
    const go = (i) => { stop(); if (i >= items.length) { play.textContent = '▶ Tinglash'; return; }
      cards.forEach((c, k) => c.classList.toggle('playing', k === i));
      audio = new Audio('https://cdn.islamic.network/quran/audio/128/ar.alafasy/' + items[i].g + '.mp3');
      audio.onended = () => go(i + 1); audio.play().catch(() => {}); play.textContent = '❚❚ To‘xtatish'; cards[i].scrollIntoView({ block: 'center', behavior: 'smooth' }); };
    play.onclick = () => { if (audio && !audio.paused) { audio.pause(); play.textContent = '▶ Davom'; } else if (audio) { audio.play(); play.textContent = '❚❚ To‘xtatish'; } else go(0); };
    if (focus) { const i = items.findIndex((x) => x.n === focus && (t === 's' || true)); if (i >= 0) cards[i].scrollIntoView({ block: 'center' }); }
  }

  window.TaqvoSections = window.TaqvoSections || {};
  window.TaqvoSections.quran = (root) => { render(root, 'surah'); return { title: 'Qur’on', status: '114 sura · audio' }; };
  window.TaqvoSections.juz = (root) => { render(root, 'juz'); return { title: 'Qur’on juzlari', status: '30 juz' }; };
})();
