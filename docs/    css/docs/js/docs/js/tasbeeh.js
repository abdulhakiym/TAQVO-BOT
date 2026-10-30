/* TAQVO PRO MAX - tasbeeh.js */
(function () {
  'use strict';
  var T = window.TAQVO;

  var MONTHS = ['yan', 'fev', 'mar', 'apr', 'may', 'iyn', 'iyl', 'avg', 'sen', 'okt', 'noy', 'dek'];
  var NOTE_PRAYER = 'Namozdan keyin 33 martadan aytish haqidagi hadis Sahih Muslim\u2019da kelgan. Maqsad sonini o\u2018zingiz o\u2018zgartirishingiz mumkin.';
  var NOTE_FREE = 'Maqsad soni shaxsiy, uni istaganingizcha o\u2018zgartiring.';

  var DHIKR = [
    { id: 'subhanalloh', short: 'Subhanalloh', ar: 'سُبْحَانَ ٱللَّهِ', tr: 'Subhanalloh',
      mean: 'Alloh (barcha kamchiliklardan) pokdir.', target: 33, note: NOTE_PRAYER },
    { id: 'alhamdulillah', short: 'Alhamdulillah', ar: 'ٱلْحَمْدُ لِلَّهِ', tr: 'Alhamdulillah',
      mean: 'Hamd (barcha maqtov) Allohgadir.', target: 33, note: NOTE_PRAYER },
    { id: 'allohuakbar', short: 'Allohu akbar', ar: 'ٱللَّهُ أَكْبَرُ', tr: 'Allohu akbar',
      mean: 'Alloh eng buyukdir.', target: 33, note: NOTE_PRAYER },
    { id: 'astagfirulloh', short: 'Astag\u2018firulloh', ar: 'أَسْتَغْفِرُ ٱللَّهَ', tr: 'Astag\u2018firulloh',
      mean: 'Allohdan mag\u2018firat so\u2018rayman.', target: 100, note: NOTE_FREE },
    { id: 'lailaha', short: 'La ilaha illalloh', ar: 'لَا إِلَٰهَ إِلَّا ٱللَّهُ', tr: 'La ilaha illalloh',
      mean: 'Allohdan boshqa iloh (ibodatga loyiq zot) yo\u2018q.', target: 100, note: NOTE_FREE },
    { id: 'salovat', short: 'Salovat', ar: 'ٱللَّهُمَّ صَلِّ عَلَىٰ مُحَمَّدٍ', tr: 'Allohumma solli ala Muhammad',
      mean: 'Ey Alloh, Muhammadga salovat (rahmat) yubor.', target: 100, note: NOTE_FREE }
  ];

  var S = null, el = null, ctx = null, armed = {}, armTimers = {};

  /* ---------- YORDAMCHI ---------- */
  function esc(s) { return T.esc(s); }
  function $(id) { return document.getElementById(id); }
  function byId(id) {
    for (var i = 0; i < DHIKR.length; i++) if (DHIKR[i].id === id) return DHIKR[i];
    return DHIKR[0];
  }
  function dayKey(d) {
    d = d || new Date();
    return d.getFullYear() + '-' + T.pad(d.getMonth() + 1) + '-' + T.pad(d.getDate());
  }
  function dayLabel(d, i) {
    if (i === 0) return 'Bugun';
    if (i === 1) return 'Kecha';
    return d.getDate() + '-' + MONTHS[d.getMonth()];
  }
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' '); }

  /* ---------- SAQLASH ---------- */
  function load() {
    var s = T.store.get('tasbeeh:state', null) || {};
    var st = { sel: DHIKR[0].id, counts: {}, targets: {}, sound: !!s.sound, vib: s.vib !== false };
    DHIKR.forEach(function (d) {
      if (s.sel === d.id) st.sel = d.id;
      var c = s.counts && s.counts[d.id];
      if (typeof c === 'number' && c >= 0 && isFinite(c)) st.counts[d.id] = Math.floor(c);
      var t = s.targets && s.targets[d.id];
      if (typeof t === 'number' && t >= 1 && t <= 100000) st.targets[d.id] = Math.floor(t);
    });
    return st;
  }
  function save() { T.store.set('tasbeeh:state', S); }
  function getDaily() {
    var d = T.store.get('tasbeeh:daily', null);
    return d && typeof d === 'object' ? d : {};
  }
  function addDaily(id) {
    var d = getDaily(), k = dayKey();
    var e = d[k] || { total: 0, by: {} };
    e.total = (e.total || 0) + 1;
    e.by = e.by || {};
    e.by[id] = (e.by[id] || 0) + 1;
    d[k] = e;
    var keys = Object.keys(d).sort().reverse();
    if (keys.length > 90) keys.slice(90).forEach(function (x) { delete d[x]; });
    T.store.set('tasbeeh:daily', d);
  }
  function target(id) { return S.targets[id] || byId(id).target; }

  /* ---------- SEZGI (tebranish, ovoz) ---------- */
  function feedback(kind) { if (S.vib) T.tg.haptic(kind); }
  function beep() {
    try {
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return;
      if (!ctx) ctx = new C();
      if (ctx.state === 'suspended') ctx.resume();
      var o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
      o.type = 'sine';
      o.frequency.value = 660;
      g.gain.setValueAtTime(0.15, t);
      g.gain.exponentialRampToValueAtTime(0.0001, t + 0.08);
      o.connect(g);
      g.connect(ctx.destination);
      o.start(t);
      o.stop(t + 0.09);
    } catch (e) {}
  }

  /* ---------- KO'RINISH ---------- */
  function renderAll() {
    var d = byId(S.sel), h = '';

    h += '<div class="tabs">' + DHIKR.map(function (x) {
      return '<button class="tab' + (x.id === S.sel ? ' active' : '') + '" data-a="sel" data-id="' + x.id + '">' + esc(x.short) + '</button>';
    }).join('') + '</div>';

    h += '<div class="card glass" style="text-align:center">' +
      '<div class="arabic" style="text-align:center;font-size:30px">' + esc(d.ar) + '</div>' +
      '<div class="translit">' + esc(d.tr) + '</div>' +
      '<div class="meaning">' + esc(d.mean) + '</div>' +
      '<div class="src">' + esc(d.note) + '</div></div>';

    h += '<div class="counter-wrap"><button class="counter-btn" id="tbBtn" data-a="tap"><span id="tbCount">0</span></button></div>';

    h += '<div class="card"><div class="row between small muted" style="margin-bottom:8px">' +
      '<span id="tbLabel"></span><span id="tbPct"></span></div>' +
      '<div class="progress"><i id="tbBar"></i></div></div>';

    h += '<div class="row" style="gap:8px"><button class="btn ghost" id="tbReset" data-a="reset">↺ Nolga qaytarish</button></div>';

    h += '<div class="card"><div style="font-weight:600;margin-bottom:8px">Maqsad soni</div>' +
      '<div class="tabs" style="margin-bottom:10px">' + [33, 99, 100, 500, 1000].map(function (n) {
        return '<button class="tab" data-a="preset" data-n="' + n + '">' + n + '</button>';
      }).join('') + '</div>' +
      '<div class="row" style="gap:8px"><input type="number" id="tbTarget" inputmode="numeric" min="1" max="100000" placeholder="Boshqa son">' +
      '<button class="btn sm" data-a="settarget" style="white-space:nowrap">Saqlash</button></div></div>';

    h += '<div class="card"><div style="font-weight:600;margin-bottom:8px">Sozlamalar</div>' +
      '<div class="row" style="gap:8px"><button class="btn sm ghost" id="tbVib" data-a="vib"></button>' +
      '<button class="btn sm ghost" id="tbSnd" data-a="snd"></button></div>' +
      '<div class="src">Tebranish Telegram ichida va qo\u2018llab-quvvatlaydigan qurilmalarda ishlaydi.</div></div>';

    h += '<div class="card" id="tbToday"></div>';
    h += '<div class="card" id="tbHist"></div>';

    el.innerHTML = h;
    updateCounter();
    updateToggles();
    renderToday();
    renderHistory();
  }

  function updateCounter() {
    var id = S.sel, c = S.counts[id] || 0, t = target(id);
    var cnt = $('tbCount'), bar = $('tbBar'), lab = $('tbLabel'), pct = $('tbPct');
    if (cnt) cnt.textContent = fmt(c);
    var p = Math.min(100, Math.round(c / t * 100));
    if (bar) bar.style.width = p + '%';
    if (lab) lab.textContent = fmt(c) + ' / ' + fmt(t) + (c >= t ? ' · Maqsad bajarildi ✓' : '');
    if (pct) pct.textContent = p + '%';
    var inp = $('tbTarget');
    if (inp && document.activeElement !== inp) inp.value = '';
    T.$$('[data-a="preset"]', el).forEach(function (b) {
      b.classList.toggle('active', +b.getAttribute('data-n') === t);
    });
  }

  function updateToggles() {
    var v = $('tbVib'), s = $('tbSnd');
    if (v) v.textContent = S.vib ? '📳 Tebranish: yoqilgan' : '📴 Tebranish: o\u2018chiq';
    if (s) s.textContent = S.sound ? '🔊 Ovoz: yoqilgan' : '🔇 Ovoz: o\u2018chiq';
  }

  function renderToday() {
    var box = $('tbToday');
    if (!box) return;
    var e = getDaily()[dayKey()] || { total: 0, by: {} };
    var h = '<div class="row between"><div style="font-weight:600">Bugungi jami</div>' +
      '<div style="font-size:24px;font-weight:700;color:var(--gold2)" id="tbTotal">' + fmt(e.total || 0) + '</div></div>';
    var rows = DHIKR.filter(function (d) { return e.by && e.by[d.id]; });
    if (rows.length) {
      h += '<div style="margin-top:8px">' + rows.map(function (d) {
        return '<div class="row between small" style="padding:4px 0"><span class="muted">' + esc(d.short) + '</span><b>' + fmt(e.by[d.id]) + '</b></div>';
      }).join('') + '</div>';
    } else {
      h += '<div class="src">Bugun hali zikr sanalmadi.</div>';
    }
    box.innerHTML = h;
  }

  function renderHistory() {
    var box = $('tbHist');
    if (!box) return;
    var daily = getDaily(), rows = [], max = 1, i;
    for (i = 0; i < 7; i++) {
      var dt = new Date();
      dt.setDate(dt.getDate() - i);
      var e = daily[dayKey(dt)];
      var tot = e && e.total ? e.total : 0;
      if (tot > max) max = tot;
      rows.push({ label: dayLabel(dt, i), total: tot });
    }
    var h = '<div class="row between" style="margin-bottom:8px"><div style="font-weight:600">So\u2018nggi 7 kun</div>' +
      '<button class="btn sm ghost" id="tbClear" data-a="clearhist">Tozalash</button></div>';
    h += rows.map(function (r) {
      return '<div class="row" style="gap:10px;padding:5px 0"><span class="small muted" style="width:52px">' + esc(r.label) + '</span>' +
        '<div class="progress grow"><i style="width:' + Math.round(r.total / max * 100) + '%"></i></div>' +
        '<b class="small" style="min-width:48px;text-align:right">' + fmt(r.total) + '</b></div>';
    }).join('');
    h += '<div class="src">Tarix faqat shu qurilmada saqlanadi.</div>';
    box.innerHTML = h;
  }

  /* ---------- HARAKATLAR ---------- */
  function tap() {
    var id = S.sel, c = (S.counts[id] || 0) + 1, t = target(id);
    S.counts[id] = c;
    addDaily(id);
    save();
    if (c === t) {
      feedback('success');
      T.toast('Mashaalloh! Maqsad bajarildi: ' + fmt(t));
    } else {
      feedback('light');
    }
    if (S.sound) beep();
    updateCounter();
    renderToday();
    var tot = $('tbHist');
    if (tot) renderHistory();
  }

  function confirmTwice(key, btn, askText, normalText, action) {
    if (armed[key]) {
      clearTimeout(armTimers[key]);
      armed[key] = false;
      btn.textContent = normalText;
      action();
      return;
    }
    armed[key] = true;
    btn.textContent = askText;
    armTimers[key] = setTimeout(function () {
      armed[key] = false;
      var b = $(btn.id);
      if (b) b.textContent = normalText;
    }, 3000);
  }

  function setTarget(n) {
    n = parseInt(n, 10);
    if (!(n >= 1 && n <= 100000)) { T.toast('1 dan 100 000 gacha son kiriting'); return; }
    S.targets[S.sel] = n;
    save();
    updateCounter();
    T.toast('Maqsad saqlandi: ' + fmt(n));
  }

  function onClick(e) {
    var b = e.target.closest('[data-a]');
    if (!b) return;
    var a = b.getAttribute('data-a');
    if (a === 'tap') tap();
    else if (a === 'sel') { S.sel = b.getAttribute('data-id'); save(); renderAll(); }
    else if (a === 'preset') setTarget(b.getAttribute('data-n'));
    else if (a === 'settarget') { var inp = $('tbTarget'); if (inp) setTarget(inp.value); }
    else if (a === 'vib') { S.vib = !S.vib; save(); updateToggles(); if (S.vib) T.tg.haptic('light'); }
    else if (a === 'snd') { S.sound = !S.sound; save(); updateToggles(); if (S.sound) beep(); }
    else if (a === 'reset') {
      confirmTwice('reset', b, 'Tasdiqlang', '↺ Nolga qaytarish', function () {
        S.counts[S.sel] = 0;
        save();
        updateCounter();
        T.toast('Sanagich nolga qaytarildi');
      });
    }
    else if (a === 'clearhist') {
      confirmTwice('hist', b, 'Tasdiqlang', 'Tozalash', function () {
        T.store.remove('tasbeeh:daily');
        renderToday();
        renderHistory();
        T.toast('Tarix tozalandi');
      });
    }
  }

  T.sections.tasbeeh = {
    title: 'Tasbeh',
    icon: '📿',
    render: function (root) {
      el = root;
      S = load();
      armed = {};
      el.onclick = onClick;
      renderAll();
    },
    leave: function () {
      Object.keys(armTimers).forEach(function (k) { clearTimeout(armTimers[k]); });
      armed = {};
      if (el) el.onclick = null;
      el = null;
    }
  };
})();
