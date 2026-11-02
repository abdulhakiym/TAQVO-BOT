/* TAQVO PRO MAX — 1-qadam: frontend skeleton
   Ishlaydi: salomlashuv, shahar tanlash, namoz vaqtlari (Aladhan API), hisoblagich, navigatsiya.
   Hali ulanmagan: Qur'on, zikr, tasbeh va boshqa bo'limlar (2-qadam), obuna tekshiruvi (3-qadam, server tomonida). */
(() => {
  const tg = window.Telegram && window.Telegram.WebApp;
  if (tg) { tg.ready(); tg.expand(); try { tg.setHeaderColor('#050507'); tg.setBackgroundColor('#050507'); } catch (e) {} }

  const $ = (id) => document.getElementById(id);
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- Sozlamalar ---------- */
  // [davlat (uz), davlat (API), hisoblash usuli, Asr maktabi (1=Hanafiy), shaharlar [uz, API]]
  const COUNTRIES = [
    ['O‘zbekiston', 'Uzbekistan', 3, 1, [['Toshkent', 'Tashkent'], ['Samarqand', 'Samarkand'], ['Buxoro', 'Bukhara'], ['Andijon', 'Andijan'], ['Namangan', 'Namangan'], ['Farg‘ona', 'Fergana'], ['Qo‘qon', 'Kokand'], ['Nukus', 'Nukus'], ['Urganch', 'Urgench'], ['Xiva', 'Khiva'], ['Qarshi', 'Karshi'], ['Termiz', 'Termez'], ['Jizzax', 'Jizzakh'], ['Navoiy', 'Navoi'], ['Guliston', 'Gulistan']]],
    ['Qirg‘iziston', 'Kyrgyzstan', 3, 1, [['Bishkek', 'Bishkek'], ['O‘sh', 'Osh'], ['Jalolobod', 'Jalal-Abad'], ['Qorako‘l', 'Karakol'], ['Norin', 'Naryn'], ['Talas', 'Talas']]],
    ['Qozog‘iston', 'Kazakhstan', 3, 1, [['Astana', 'Astana'], ['Almati', 'Almaty'], ['Shimkent', 'Shymkent'], ['Turkiston', 'Turkistan'], ['Oqtobe', 'Aktobe']]],
    ['Tojikiston', 'Tajikistan', 3, 1, [['Dushanbe', 'Dushanbe'], ['Xo‘jand', 'Khujand'], ['Ko‘lob', 'Kulob'], ['Bo‘xtar', 'Bokhtar']]],
    ['Turkmaniston', 'Turkmenistan', 3, 1, [['Ashxobod', 'Ashgabat'], ['Turkmanobod', 'Turkmenabat'], ['Dashog‘uz', 'Dashoguz']]],
    ['Rossiya', 'Russia', 14, 1, [['Moskva', 'Moscow'], ['Sankt-Peterburg', 'Saint Petersburg'], ['Qozon', 'Kazan'], ['Ufa', 'Ufa'], ['Grozniy', 'Grozny'], ['Mahachqal‘a', 'Makhachkala'], ['Yekaterinburg', 'Yekaterinburg'], ['Novosibirsk', 'Novosibirsk']]],
    ['Turkiya', 'Turkey', 13, 1, [['Istanbul', 'Istanbul'], ['Anqara', 'Ankara'], ['Izmir', 'Izmir'], ['Konya', 'Konya']]],
    ['Saudiya Arabistoni', 'Saudi Arabia', 4, 0, [['Makka', 'Makkah'], ['Madina', 'Medina'], ['Ar-Riyod', 'Riyadh']]],
    ['Germaniya', 'Germany', 3, 1, [['Berlin', 'Berlin'], ['Kyoln', 'Cologne'], ['Myunxen', 'Munich']]]
  ];
  // city = [shahar(uz), shahar(API), davlat(API), davlat(uz), usul, maktab]
  const CITIES = COUNTRIES.flatMap(k => k[4].map(c => [c[0], c[1], k[1], k[0], k[2], k[3]]));
  const PRAYERS = [['Fajr', 'Bomdod'], ['Dhuhr', 'Peshin'], ['Asr', 'Asr'], ['Maghrib', 'Shom'], ['Isha', 'Xufton']];

  const SECTIONS = [
    ['quran', '📖', 'Qur’on'], ['prayer', '🕌', 'Namoz vaqtlari'], ['tasbeh', '📿', 'Tasbeh'],
    ['morning', '🌅', 'Tonggi zikr'], ['evening', '🌙', 'Kechki zikr'], ['duas', '🤲', 'Duolar'],
    ['hadith', '📜', 'Sahih hadis'], ['knowledge', '🎓', 'Islomiy bilim'], ['ai', '✨', 'TAQVO AI'],
    ['quiz', '❓', 'Viktorina'], ['farz', '☪️', 'Farz amallar'], ['siyrat', '🕋', 'Siyrat'],
    ['fiqh', '⚖️', 'Fiqh'], ['names', '🌟', 'Allohning 99 ismi'], ['juz', '📚', 'Qur’on juzlari'],
    ['media', '🎬', 'Islomiy media'], ['leaderboard', '🏆', 'Reyting']
  ];

  /* ---------- Salomlashuv ---------- */
  const user = tg && tg.initDataUnsafe && tg.initDataUnsafe.user;
  // Faqat ko'rsatish uchun. Haqiqiy foydalanuvchi identifikatsiyasi serverda initData orqali tekshiriladi (3-qadam).
  $('hello').textContent = 'Assalomu alaykum' + (user && user.first_name ? ', ' + user.first_name : '');

  /* ---------- Shahar ---------- */
  let city = store.get('city2', CITIES[0]);
  $('cityName').textContent = city[0];

  const sheet = $('sheet'), list = $('cityList'), search = $('citySearch');
  function renderCities(q) {
    q = (q || '').trim().toLowerCase();
    list.innerHTML = '';
    const rows = CITIES.filter(c => (c[0] + c[1] + c[2] + c[3]).toLowerCase().includes(q));
    if (!rows.length) { list.innerHTML = '<li class="empty">Shahar topilmadi. Boshqa nom bilan qidiring.</li>'; return; }
    let last = '';
    rows.forEach(c => {
      if (c[3] !== last) { last = c[3]; const g = document.createElement('li'); g.className = 'grp'; g.textContent = c[3]; list.appendChild(g); }
      const li = document.createElement('li');
      if (c[1] === city[1] && c[2] === city[2]) li.className = 'sel';
      const b = document.createElement('button');
      b.textContent = c[0];
      b.onclick = () => { city = c; store.set('city2', c); $('cityName').textContent = c[0]; closeSheet(); loadPrayers(); };
      li.appendChild(b); list.appendChild(li);
    });
  }
  function openSheet() { sheet.hidden = false; search.value = ''; renderCities(''); }
  function closeSheet() { sheet.hidden = true; }
  $('cityBtn').onclick = openSheet;
  $('sheetClose').onclick = closeSheet;
  sheet.addEventListener('click', (e) => { if (e.target === sheet) closeSheet(); });
  search.addEventListener('input', () => renderCities(search.value));

  /* ---------- Namoz vaqtlari (Aladhan API, qattiq yozilmagan) ---------- */
  let times = null, tz = 'Asia/Tashkent';

  async function loadPrayers() {
    const note = $('prayerNote');
    note.className = 'note'; note.textContent = 'Yuklanmoqda…';
    const key = 'pt:' + city[1] + city[2] + ':' + new Date().toDateString();
    try {
      const url = 'https://api.aladhan.com/v1/timingsByCity?city=' + encodeURIComponent(city[1]) +
        '&country=' + encodeURIComponent(city[2]) + '&method=' + city[4] + '&school=' + city[5];
      const r = await fetch(url);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const j = await r.json();
      const t = j.data.timings;
      times = {}; PRAYERS.forEach(p => { times[p[0]] = String(t[p[0]]).slice(0, 5); });
      tz = j.data.meta.timezone || tz;
      store.set(key, { times, tz });
      note.textContent = '';
    } catch (e) {
      const c = store.get(key, null);
      if (c) { times = c.times; tz = c.tz; note.textContent = 'Internet yo‘q: saqlangan vaqtlar ko‘rsatilmoqda.'; }
      else { times = null; note.className = 'note err'; note.textContent = 'Namoz vaqtlarini olib bo‘lmadi. Internetni tekshirib, shaharni qayta tanlang.'; }
    }
    renderPrayers(); tick();
  }

  function toSec(hm) { const [h, m] = hm.split(':').map(Number); return h * 3600 + m * 60; }
  function nowSec() {
    const p = new Intl.DateTimeFormat('en-GB', { timeZone: tz, hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' })
      .format(new Date()).split(':').map(Number);
    return p[0] * 3600 + p[1] * 60 + p[2];
  }
  function nextPrayer() {
    const n = nowSec();
    for (let i = 0; i < PRAYERS.length; i++) { const s = toSec(times[PRAYERS[i][0]]); if (s > n) return { i, left: s - n }; }
    return { i: 0, left: toSec(times.Fajr) + 86400 - n }; // ertangi Bomdod (taxminiy, ertasi kuni yangilanadi)
  }
  const pad = (x) => String(x).padStart(2, '0');

  function renderPrayers() {
    const box = $('prayers'); box.innerHTML = '';
    PRAYERS.forEach(p => {
      const d = document.createElement('div'); d.className = 'p'; d.dataset.k = p[0];
      d.innerHTML = '<b>' + p[1] + '</b><span>' + (times ? times[p[0]] : '--:--') + '</span>';
      box.appendChild(d);
    });
  }
  function tick() {
    if (!times) { $('nextName').textContent = '—'; $('countdown').textContent = '--:--:--'; $('nextAt').textContent = ''; return; }
    const nx = nextPrayer(), k = PRAYERS[nx.i];
    $('nextName').textContent = k[1];
    $('nextAt').textContent = times[k[0]] + ' da';
    $('countdown').textContent = pad(Math.floor(nx.left / 3600)) + ':' + pad(Math.floor(nx.left % 3600 / 60)) + ':' + pad(nx.left % 60);
    document.querySelectorAll('.p').forEach(el => el.classList.toggle('next', el.dataset.k === k[0]));
  }
  setInterval(tick, 1000);

  /* ---------- Bo'limlar va navigatsiya ---------- */
  const grid = $('grid');
  SECTIONS.forEach(s => {
    const b = document.createElement('button'); b.className = 'tile'; b.dataset.open = s[0];
    b.innerHTML = '<i>' + s[1] + '</i>' + s[2];
    grid.appendChild(b);
  });

  const home = $('home'), view = $('view');
  function show(page) { home.classList.toggle('active', page === home); view.classList.toggle('active', page === view); window.scrollTo(0, 0); }

  function open(id) {
    if (id === 'prayer') { goHome(); return; } // namoz vaqtlari bosh sahifada ishlaydi
    const s = SECTIONS.find(x => x[0] === id); if (!s) return;
    $('viewTitle').textContent = s[2];
    $('viewStatus').textContent = 'Hali ulanmagan';
    $('viewBody').innerHTML = '<div class="empty">Bu bo‘lim keyingi qadamda to‘liq ishga tushadi. Hozir faqat bosh sahifa va namoz vaqtlari ishlaydi.</div>';
    show(view);
    if (tg) { tg.BackButton.show(); }
  }
  function goHome() { show(home); if (tg) tg.BackButton.hide(); }

  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-open]'); if (t) open(t.dataset.open);
  });
  $('backBtn').onclick = goHome;
  if (tg) tg.BackButton.onClick(goHome);

  loadPrayers();
})();
