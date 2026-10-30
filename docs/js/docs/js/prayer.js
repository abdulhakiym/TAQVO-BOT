/* TAQVO PRO MAX - prayer.js */
(function () {
  'use strict';
  var T = window.TAQVO;

  var KEYS = ['Fajr', 'Sunrise', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];
  var NAMES = { Fajr: 'Bomdod', Sunrise: 'Quyosh', Dhuhr: 'Peshin', Asr: 'Asr', Maghrib: 'Shom', Isha: 'Xufton' };
  var NOTIFY_KEYS = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];

  var METHODS = [
    { id: 1, name: 'Karachi (Islomiy fanlar universiteti)' },
    { id: 3, name: 'Muslim World League' },
    { id: 2, name: 'ISNA (Shimoliy Amerika)' },
    { id: 4, name: 'Umm al-Qura (Makka)' },
    { id: 5, name: 'Misr umumiy geodeziya boshqarmasi' },
    { id: 13, name: 'Diyanet (Turkiya)' },
    { id: 14, name: 'Rossiya musulmonlari ma\'muriyati' }
  ];
  var SCHOOLS = [
    { id: 1, name: 'Hanafiy (Asr kechroq)' },
    { id: 0, name: 'Shofiiy, Molikiy, Hanbaliy (Asr ertaroq)' }
  ];

  var CITIES = [
    { name: 'Toshkent', country: 'O\'zbekiston', lat: 41.2995, lng: 69.2401, tz: 'Asia/Tashkent' },
    { name: 'Samarqand', country: 'O\'zbekiston', lat: 39.6270, lng: 66.9750, tz: 'Asia/Samarkand' },
    { name: 'Buxoro', country: 'O\'zbekiston', lat: 39.7747, lng: 64.4286, tz: 'Asia/Samarkand' },
    { name: 'Andijon', country: 'O\'zbekiston', lat: 40.7821, lng: 72.3442, tz: 'Asia/Tashkent' },
    { name: 'Namangan', country: 'O\'zbekiston', lat: 40.9983, lng: 71.6726, tz: 'Asia/Tashkent' },
    { name: 'Farg\'ona', country: 'O\'zbekiston', lat: 40.3864, lng: 71.7864, tz: 'Asia/Tashkent' },
    { name: 'Qo\'qon', country: 'O\'zbekiston', lat: 40.5286, lng: 70.9425, tz: 'Asia/Tashkent' },
    { name: 'Marg\'ilon', country: 'O\'zbekiston', lat: 40.4711, lng: 71.7247, tz: 'Asia/Tashkent' },
    { name: 'Qarshi', country: 'O\'zbekiston', lat: 38.8606, lng: 65.7891, tz: 'Asia/Samarkand' },
    { name: 'Navoiy', country: 'O\'zbekiston', lat: 40.0844, lng: 65.3792, tz: 'Asia/Samarkand' },
    { name: 'Jizzax', country: 'O\'zbekiston', lat: 40.1158, lng: 67.8422, tz: 'Asia/Samarkand' },
    { name: 'Guliston', country: 'O\'zbekiston', lat: 40.4897, lng: 68.7842, tz: 'Asia/Tashkent' },
    { name: 'Termiz', country: 'O\'zbekiston', lat: 37.2242, lng: 67.2783, tz: 'Asia/Samarkand' },
    { name: 'Urganch', country: 'O\'zbekiston', lat: 41.5500, lng: 60.6333, tz: 'Asia/Samarkand' },
    { name: 'Xiva', country: 'O\'zbekiston', lat: 41.3783, lng: 60.3639, tz: 'Asia/Samarkand' },
    { name: 'Nukus', country: 'O\'zbekiston', lat: 42.4531, lng: 59.6103, tz: 'Asia/Samarkand' },
    { name: 'Dushanbe', country: 'Tojikiston', lat: 38.5598, lng: 68.7870, tz: 'Asia/Dushanbe' },
    { name: 'Bishkek', country: 'Qirg\'iziston', lat: 42.8746, lng: 74.5698, tz: 'Asia/Bishkek' },
    { name: 'Almati', country: 'Qozog\'iston', lat: 43.2220, lng: 76.8512, tz: 'Asia/Almaty' },
    { name: 'Moskva', country: 'Rossiya', lat: 55.7558, lng: 37.6173, tz: 'Europe/Moscow' },
    { name: 'Istanbul', country: 'Turkiya', lat: 41.0082, lng: 28.9784, tz: 'Europe/Istanbul' },
    { name: 'Makka', country: 'Saudiya Arabistoni', lat: 21.4225, lng: 39.8262, tz: 'Asia/Riyadh' },
    { name: 'Madina', country: 'Saudiya Arabistoni', lat: 24.4672, lng: 39.6111, tz: 'Asia/Riyadh' },
    { name: 'Qohira', country: 'Misr', lat: 30.0444, lng: 31.2357, tz: 'Africa/Cairo' }
  ];

  var DEFAULT_SETTINGS = { method: 1, school: 1 };
  var DEFAULT_NOTIFY = {
    on: false, before: 10,
    prayers: { Fajr: true, Dhuhr: true, Asr: true, Maghrib: true, Isha: true }
  };

  var S = {
    city: null, settings: null,
    today: null, tomorrow: null, dayKey: '',
    loading: false, error: false,
    req: 0, lastTry: 0,
    tomorrowBusy: false, tomorrowFail: 0,
    nextKey: null, pageEl: null
  };

  /* ---------- YORDAMCHI ---------- */
  function pad(n) { return T.pad(n); }
  function esc(s) { return T.esc(s); }
  function setText(id, txt) { var e = document.getElementById(id); if (e) e.textContent = txt; }
  function toSec(hhmm) { var p = hhmm.split(':'); return (+p[0]) * 3600 + (+p[1]) * 60; }
  function fmtCount(sec) {
    if (sec < 0) sec = 0;
    return pad(Math.floor(sec / 3600)) + ':' + pad(Math.floor((sec % 3600) / 60)) + ':' + pad(sec % 60);
  }
  function dateStr(o) { return pad(o.d) + '-' + pad(o.m) + '-' + o.y; }
  function addDay(n) {
    var dt = new Date(Date.UTC(n.y, n.m - 1, n.d + 1));
    return { y: dt.getUTCFullYear(), m: dt.getUTCMonth() + 1, d: dt.getUTCDate() };
  }
  function norm(s) { return String(s).toLowerCase().replace(/['’ʻʼ`]/g, ''); }

  // Shahar vaqt mintaqasidagi hozirgi vaqt
  function nowIn(tz) {
    var opt = { hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
    var parts;
    try {
      if (tz) opt.timeZone = tz;
      parts = new Intl.DateTimeFormat('en-GB', opt).formatToParts(new Date());
    } catch (e) {
      delete opt.timeZone;
      parts = new Intl.DateTimeFormat('en-GB', opt).formatToParts(new Date());
    }
    var o = {};
    parts.forEach(function (p) { if (p.type !== 'literal') o[p.type] = parseInt(p.value, 10); });
    if (o.hour === 24) o.hour = 0;
    return { y: o.year, m: o.month, d: o.day, h: o.hour, mi: o.minute, s: o.second };
  }

  /* ---------- API ---------- */
  function apiUrl(ymd) {
    var c = S.city;
    var u = T.config.ALADHAN + '/timings/' + dateStr(ymd) +
      '?latitude=' + c.lat + '&longitude=' + c.lng +
      '&method=' + S.settings.method + '&school=' + S.settings.school;
    if (c.tz) u += '&timezonestring=' + encodeURIComponent(c.tz);
    return u;
  }

  function fetchDay(ymd) {
    return T.cachedJSON(apiUrl(ymd), 6 * 3600 * 1000, { timeout: 12000, retries: 1 }).then(function (res) {
      if (!res || res.code !== 200 || !res.data || !res.data.timings) throw new Error('bad response');
      var tm = res.data.timings, t = {};
      KEYS.forEach(function (k) {
        var m = String(tm[k] || '').match(/(\d{1,2}):(\d{2})/);
        if (!m) throw new Error('bad time');
        t[k] = pad(+m[1]) + ':' + m[2];
      });
      var h = res.data.date && res.data.date.hijri;
      var meta = res.data.meta || {};
      return {
        t: t,
        hijri: h ? (parseInt(h.day, 10) + ' ' + ((h.month && h.month.en) || '') + ' ' + h.year + '-yil') : '',
        method: (meta.method && meta.method.name) || '',
        tz: meta.timezone || ''
      };
    });
  }

  function load() {
    var req = ++S.req;
    S.loading = true; S.error = false; S.tomorrow = null; S.lastTry = Date.now();
    applyState();
    var n = nowIn(S.city.tz);
    var key = n.y + '-' + n.m + '-' + n.d;
    return fetchDay(n).then(function (r) {
      if (req !== S.req) return;
      S.today = r; S.dayKey = key;
      if (!S.city.tz && r.tz) { S.city.tz = r.tz; T.store.set('prayer:city', S.city); }
      S.loading = false; S.error = false;
      renderHome(); applyState(); refreshPage(); tick();
    }).catch(function () {
      if (req !== S.req) return;
      S.loading = false; S.error = true;
      applyState(); refreshPage();
    });
  }

  function loadTomorrow() {
    if (S.tomorrowBusy) return;
    if (S.tomorrowFail && Date.now() - S.tomorrowFail < 30000) return;
    S.tomorrowBusy = true;
    var req = S.req;
    fetchDay(addDay(nowIn(S.city.tz))).then(function (r) {
      if (req === S.req) S.tomorrow = r;
    }).catch(function () {
      S.tomorrowFail = Date.now();
    }).then(function () {
      S.tomorrowBusy = false;
    });
  }

  /* ---------- KO'RINISH ---------- */
  function stateInfo() {
    if (S.loading && !S.today) return { c: 'state', h: 'Namoz vaqtlari yuklanmoqda…' };
    if (S.error && !S.today) {
      return { c: 'state err', h: '⚠️ Namoz vaqtlarini yuklab bo\'lmadi. Internetni tekshiring.<br><br><button class="btn sm" data-act="prayer-retry">Qayta urinish</button>' };
    }
    if (S.error) return { c: 'state err', h: 'Yangilab bo\'lmadi. Oxirgi yuklangan vaqtlar ko\'rsatilmoqda.' };
    return { c: 'state', h: '' };
  }

  function applyState() {
    var info = stateInfo();
    ['prayerState', 'pgState'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) { el.className = info.c; el.innerHTML = info.h; }
    });
  }

  function renderHome() {
    setText('cityName', S.city.name);
    setText('methodName', S.today && S.today.method ? S.today.method : '');
    setText('dateH', S.today && S.today.hijri ? S.today.hijri : '—');
    var g = document.getElementById('timesGrid');
    if (!g) return;
    g.innerHTML = S.today ? KEYS.map(function (k) {
      return '<div class="time-box" data-k="' + k + '"><div class="n">' + NAMES[k] +
        '</div><div class="t">' + S.today.t[k] + '</div></div>';
    }).join('') : '';
    highlight();
  }

  function highlight() {
    T.$$('.time-box').forEach(function (b) {
      b.classList.toggle('on', !!S.nextKey && b.getAttribute('data-k') === S.nextKey);
    });
  }

  function tick() {
    if (!S.today) {
      setText('nextName', '—'); setText('countdown', '--:--:--');
      setText('pgNext', '—'); setText('pgCount', '--:--:--');
      return;
    }
    var n = nowIn(S.city.tz);
    var key = n.y + '-' + n.m + '-' + n.d;
    if (key !== S.dayKey) {
      if (!S.loading && Date.now() - S.lastTry > 30000) load();
      return;
    }
    var sec = n.h * 3600 + n.mi * 60 + n.s;
    var nextKey = null, left = 0, name = '—', nextToday = null;
    for (var i = 0; i < KEYS.length; i++) {
      var ts = toSec(S.today.t[KEYS[i]]);
      if (ts > sec) { nextToday = KEYS[i]; left = ts - sec; break; }
    }
    if (nextToday) {
      nextKey = nextToday; name = NAMES[nextToday];
    } else if (S.tomorrow) {
      left = 86400 - sec + toSec(S.tomorrow.t.Fajr);
      name = 'Bomdod (ertaga)';
    } else {
      loadTomorrow();
      setText('nextName', '—'); setText('countdown', '--:--:--');
      setText('pgNext', '—'); setText('pgCount', '--:--:--');
      S.nextKey = null; highlight();
      return;
    }
    var cd = fmtCount(left);
    setText('nextName', name); setText('countdown', cd);
    setText('pgNext', name); setText('pgCount', cd);
    if (S.nextKey !== nextKey) { S.nextKey = nextKey; highlight(); }
  }

  /* ---------- SHAHAR TANLASH ---------- */
  function renderCityList(filter) {
    var list = document.getElementById('cityList');
    if (!list) return;
    var f = norm(filter || '');
    var html = CITIES.filter(function (c) { return norm(c.name).indexOf(f) > -1; }).map(function (c) {
      var on = S.city && !S.city.gps && S.city.name === c.name;
      return '<button class="city-item' + (on ? ' on' : '') + '" data-city="' + esc(c.name) + '">' +
        esc(c.name) + ' <span class="muted small">' + esc(c.country) + '</span></button>';
    }).join('');
    list.innerHTML = html || '<div class="empty">Shahar topilmadi</div>';
  }

  function openSheet() {
    var sh = document.getElementById('citySheet');
    var inp = document.getElementById('cityFilter');
    if (!sh) return;
    if (inp) inp.value = '';
    renderCityList('');
    sh.classList.add('open');
  }
  function closeSheet() {
    var sh = document.getElementById('citySheet');
    if (sh) sh.classList.remove('open');
  }

  function applyCity(c) {
    S.city = c;
    T.store.set('prayer:city', c);
    S.today = null; S.tomorrow = null; S.nextKey = null;
    renderHome(); tick(); refreshPage();
    load();
  }

  function selectCity(name) {
    for (var i = 0; i < CITIES.length; i++) {
      if (CITIES[i].name === name) {
        var c = CITIES[i];
        applyCity({ name: c.name, lat: c.lat, lng: c.lng, tz: c.tz });
        closeSheet();
        T.tg.haptic('light');
        return;
      }
    }
  }

  function useGPS() {
    if (!navigator.geolocation) { T.toast('Qurilmangiz GPS\'ni qo\'llab-quvvatlamaydi'); return; }
    T.toast('Joylashuv aniqlanmoqda…');
    navigator.geolocation.getCurrentPosition(function (p) {
      applyCity({
        name: 'Joylashuvim (GPS)',
        lat: +p.coords.latitude.toFixed(4),
        lng: +p.coords.longitude.toFixed(4),
        tz: null, gps: true
      });
      closeSheet();
    }, function () {
      T.toast('Joylashuvga ruxsat berilmadi. Shaharni qo\'lda tanlang.');
    }, { timeout: 10000, maximumAge: 600000 });
  }

  /* ---------- ESLATMA SOZLAMALARI (faqat qurilmada saqlanadi) ---------- */
  function getNotify() {
    var s = T.store.get('prayer:notify', null) || {};
    var out = { on: !!s.on, before: typeof s.before === 'number' ? s.before : DEFAULT_NOTIFY.before, prayers: {} };
    NOTIFY_KEYS.forEach(function (k) {
      out.prayers[k] = s.prayers && typeof s.prayers[k] === 'boolean' ? s.prayers[k] : true;
    });
    return out;
  }
  function setNotify(n) { T.store.set('prayer:notify', n); }

  /* ---------- NAMOZ VAQTLARI SAHIFASI ---------- */
  function opts(list, sel) {
    return list.map(function (o) {
      return '<option value="' + o.id + '"' + (o.id === sel ? ' selected' : '') + '>' + esc(o.name) + '</option>';
    }).join('');
  }

  function buildPage() {
    var el = S.pageEl;
    if (!el) return;
    var nt = getNotify();
    var h = '';

    h += '<div class="card glass">';
    h += '<div class="row between"><button class="city-btn" data-act="city">📍 ' + esc(S.city.name) + ' ▾</button>';
    h += '<span class="chip">' + esc(S.today ? S.today.hijri : '') + '</span></div>';
    h += '<div class="next"><div class="muted small">Keyingi namoz</div>';
    h += '<div class="next-name" id="pgNext">—</div><div class="countdown" id="pgCount">--:--:--</div></div>';
    h += '<div class="state" id="pgState"></div></div>';

    h += '<div class="card"><div class="muted small" style="margin-bottom:8px">Bugungi jadval · ' + esc(T.formatDate(new Date())) + '</div>';
    h += KEYS.map(function (k) {
      return '<div class="row between time-box" data-k="' + k + '" style="padding:12px 14px;margin-bottom:6px">' +
        '<span>' + NAMES[k] + '</span><b class="t">' + (S.today ? S.today.t[k] : '--:--') + '</b></div>';
    }).join('');
    if (S.today && S.today.method) h += '<div class="src">Hisoblash usuli: ' + esc(S.today.method) + '</div>';
    h += '<div class="src">Manba: AlAdhan API. Mahalliy masjid jadvali bilan solishtirib ko\'ring.</div></div>';

    h += '<div class="card"><h3 style="margin-bottom:10px">Hisoblash sozlamalari</h3>';
    h += '
