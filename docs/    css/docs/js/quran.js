/* TAQVO PRO MAX - quran.js (Qur'oni Karim, 30 pora, qorilar) */
(function () {
  'use strict';
  var T = window.TAQVO;

  var TR_ED = 'uz.sodik'; // o'zbekcha tarjima nashri (alquran.cloud)
  var SILENT = 'data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=';

  var RECITERS = [
    { id: 'ar.alafasy', name: 'Mishary Rashid Alafasy', ar: 'مشاري راشد العفاسي' },
    { id: 'ar.abdurrahmaansudais', name: 'Abdul Rahman Al-Sudais', ar: 'عبد الرحمن السديس' },
    { id: 'ar.husary', name: 'Mahmoud Khalil Al-Husary', ar: 'محمود خليل الحصري' },
    { id: 'ar.minshawi', name: 'Muhammad Siddiq Al-Minshawi', ar: 'محمد صديق المنشاوي' },
    { id: 'ar.mahermuaiqly', name: 'Maher Al-Muaiqly', ar: 'ماهر المعيقلي' },
    { id: 'ar.ahmedajamy', name: 'Ahmed Al-Ajmi', ar: 'أحمد العجمي' }
  ];

  var P = null;          // ochiq sahifa holati
  var R = null;          // ochiq o'qish oynasi holati
  var obs = null, saveTimer = null, pending = null, surahsCache = null;
  var Q = { audio: null, unlocked: false, n: 0, i: -1, token: 0, playing: false,
            getUrl: null, onActive: null, label: null, maps: {} };

  function esc(s) { return T.esc(s); }

  /* ---------- YORDAMCHI ---------- */
  function api(path) {
    return T.cachedJSON(T.config.QURAN + path, 30 * 24 * 3600 * 1000, { timeout: 15000, retries: 1 })
      .then(function (res) {
        if (!res || res.code !== 200 || !res.data) throw new Error('bad');
        return res.data;
      });
  }
  function stripDia(s) { return String(s).replace(/[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]/g, ''); }
  function norm(s) { return String(s).toLowerCase().replace(/[^a-z0-9]/g, ''); }
  function getReciter() {
    var id = T.store.get('quran:reciter', RECITERS[0].id);
    for (var i = 0; i < RECITERS.length; i++) if (RECITERS[i].id === id) return RECITERS[i];
    return RECITERS[0];
  }

  // Kirill -> Lotin (taxminiy, avtomatik)
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
      } else {
        v = C2L[lo];
      }
      if (v === undefined) { out += ch; continue; }
      out += (up && v.length) ? v.charAt(0).toUpperCase() + v.slice(1) : v;
    }
    return out;
  }

  /* ---------- MA'LUMOT ---------- */
  function loadSurahs() {
    if (surahsCache) return Promise.resolve(surahsCache);
    return api('/surah').then(function (d) { surahsCache = d; return d; });
  }

  function fetchEditions(kind, n) {
    var base = '/' + kind + '/' + n;
    return api(base + '/editions/quran-uthmani,' + TR_ED).catch(function () {
      return Promise.all([
        api(base + '/quran-uthmani'),
        api(base + '/' + TR_ED).catch(function () { return null; })
      ]).then(function (r) { return r[1] ? [r[0], r[1]] : [r[0]]; });
    });
  }

  function loadText(kind, n) {
    return fetchEditions(kind, n).then(function (d) {
      var arEd = d[0], trEd = d.length > 1 ? d[1] : null, tr = {};
      if (trEd) trEd.ayahs.forEach(function (a) { tr[a.number] = a.text; });
      var list = arEd.ayahs.map(function (a) {
        var isS = kind === 'surah';
        return {
          g: a.number, n: a.numberInSurah,
          s: isS ? arEd.number : (a.surah ? a.surah.number : 0),
          sn: isS ? arEd.englishName : (a.surah ? a.surah.englishName : ''),
          sa: isS ? arEd.name : (a.surah ? a.surah.name : ''),
          ar: a.text, tr: tr[a.number] || '', bismText: ''
        };
      });
      // Birinchi oyat matnidagi Bismillahni ajratamiz (Fotiha va Tavbadan tashqari)
      list.forEach(function (a) {
        if (a.n === 1 && a.s !== 1 && a.s !== 9) {
          var w = a.ar.split(' ');
          if (w.length > 4 && stripDia(w[0]) === 'بسم') {
            a.bismText = w.slice(0, 4).join(' ');
            a.ar = w.slice(4).join(' ');
          }
        }
      });
      return { kind: kind, n: n, info: arEd, ayahs: list, source: trEd ? trEd.edition : null };
    });
  }

  /* ---------- BELGILAR ---------- */
  function bmList() { return T.store.get('quran:bm', []) || []; }
  function isBm(s, n) { return bmList().some(function (b) { return b.s === s && b.n === n; }); }
  function toggleBm(a) {
    var l = bmList(), idx = -1;
    l.forEach(function (b, k) { if (b.s === a.s && b.n === a.n) idx = k; });
    if (idx > -1) { l.splice(idx, 1); T.store.set('quran:bm', l); return false; }
    l.unshift({ s: a.s, n: a.n, sn: a.sn, t: Date.now() });
    T.store.set('quran:bm', l);
    return true;
  }

  /* ---------- AUDIO ---------- */
  function ensureAudio() {
    if (Q.audio) return;
    var a = new Audio();
    a.preload = 'auto';
    a.addEventListener('ended', function () {
      if (Q.i + 1 < Q.n) playAt(Q.i + 1);
      else { Q.playing = false; setBar(); }
    });
    a.addEventListener('playing', function () { Q.playing = true; setBar(); });
    a.addEventListener('pause', function () { Q.playing = false; setBar(); });
    Q.audio = a;
  }
  function unlock() {
    ensureAudio();
    if (Q.unlocked) return;
    Q.unlocked = true;
    try {
      Q.audio.src = SILENT;
      var p = Q.audio.play();
      if (p && p.catch) p.catch(function () {});
    } catch (e) {}
  }
  function setBar() {
    var b = document.getElementById('qpBtn');
    if (b) b.textContent = Q.playing ? '⏸' : '▶';
    var l = document.getElementById('qpLabel');
    if (l) l.textContent = (Q.i >= 0 && Q.label) ? Q.label(Q.i) : 'Oyatni tanlang yoki ▶ bosing';
  }
  function setupQueue(n, getUrl, onActive, label) {
    stopAudio();
    Q.n = n; Q.getUrl = getUrl; Q.onActive = onActive; Q.label = label; Q.i = -1;
    setBar();
  }
  function playAt(i) {
    ensureAudio();
    if (i < 0 || i >= Q.n) return;
    Q.i = i;
    var tk = ++Q.token;
    if (Q.onActive) Q.onActive(i);
    setBar();
    Q.getUrl(i).then(function (url) {
      if (tk !== Q.token) return;
      if (!url) throw new Error('nourl');
      Q.audio.src = url;
      var p = Q.audio.play();
      if (p && p.catch) p.catch(function () {
        Q.playing = false; setBar();
        T.toast('Ovozni ijro etib bo\u2018lmadi');
      });
    }).catch(function () {
      if (tk !== Q.token) return;
      Q.playing = false; setBar();
      T.toast('Audio yuklanmadi. Internetni yoki tanlangan qorini tekshiring.');
    });
  }
  function toggle() {
    ensureAudio();
    if (Q.i < 0) { unlock(); playAt(0); return; }
    if (Q.audio.paused) {
      var p = Q.audio.play();
      if (p && p.catch) p.catch(function () {});
    } else Q.audio.pause();
  }
  function stopAudio() {
    Q.token++;
    if (Q.audio) {
      try { Q.audio.pause(); Q.audio.removeAttribute('src'); Q.audio.load(); } catch (e) {}
    }
    Q.i = -1; Q.playing = false;
    if (Q.onActive) Q.onActive(-1);
    setBar();
  }
  function urlMap(kind, n, rec) {
    var key = kind + ':' + n + ':' + rec;
    if (!Q.maps[key]) {
      Q.maps[key] = T.getJSON(T.config.QURAN + '/' + kind + '/' + n + '/' + rec, { timeout: 15000, retries: 1 })
        .then(function (res) {
          if (!res || res.code !== 200 || !res.data) throw new Error('bad');
          var m = {};
          (res.data.ayahs || []).forEach(function (a) { if (a.audio) m[a.number] = a.audio; });
          return m;
        }).catch(function (e) { delete Q.maps[key]; throw e; });
    }
    return Q.maps[key];
  }
  function playerHTML() {
    return '<div class="player glass" id="qPlayer">' +
      '<button class="icon-btn" data-a="prev">⏮</button>' +
      '<button class="icon-btn on" id="qpBtn" data-a="toggle">▶</button>' +
      '<button class="icon-btn" data-a="next">⏭</button>' +
      '<div class="grow small muted" id="qpLabel">Oyatni tanlang yoki ▶ bosing</div></div>';
  }

  /* ---------- SURALAR RO'YXATI ---------- */
  function showList(tab) {
    if (!P) return;
    P.mode = 'list'; P.tab = tab || P.tab || 'surahs';
    R = null; stopAudio(); unwatch();
    var el = P.el, h = '';
    h += '<div class="tabs"><button class="tab' + (P.tab === 'surahs' ? ' active' : '') + '" data-a="tab" data-t="surahs">Suralar</button>' +
         '<button class="tab' + (P.tab === 'bm' ? ' active' : '') + '" data-a="tab" data-t="bm">Belgilanganlar</button></div>';
    if (P.tab === 'surahs') {
      var last = T.store.get('quran:last', null);
      if (last && last.s) {
        h += '<div class="card glass"><div class="muted small">Oxirgi o\u2018qilgan joy</div>' +
          '<div style="margin:4px 0 10px;font-weight:600">' + esc(last.sn) + ' · ' + last.n + '-oyat</div>' +
          '<button class="btn" data-a="cont">Davom etish</button></div>';
      }
      h += '<input type="search" id="qSearch" placeholder="Sura qidirish (nomi yoki raqami)…" autocomplete="off">';
      h += '<div id="sList">' + T.loaderHTML + '</div>';
      el.innerHTML = h;
      loadSurahs().then(function (l) { if (P && P.el === el) { P.surahs = l; fillList(''); } })
        .catch(function () {
          var b = document.getElementById('sList');
          if (b) b.innerHTML = T.errorHTML('Suralar ro\u2018yxatini yuklab bo\u2018lmadi', 'qRetry');
        });
    } else {
      var l = bmList();
      if (!l.length) h += '<div class="empty">Hozircha belgilangan oyat yo\u2018q.<br>Oyat yonidagi ☆ tugmasini bosing.</div>';
      l.forEach(function (b) {
        h += '<div class="row"><button class="list-item grow" data-a="bmopen" data-s="' + b.s + '" data-n="' + b.n + '">' +
          '<span class="num">' + b.s + '</span><span class="grow">' + esc(b.sn) + '<div class="muted small">' + b.n + '-oyat</div></span></button>' +
          '<button class="icon-btn" data-a="bmdel" data-s="' + b.s + '" data-n="' + b.n + '">✕</button></div>';
      });
      el.innerHTML = h;
    }
  }

  function fillList(f) {
    var box = document.getElementById('sList');
    if (!box || !P || !P.surahs) return;
    var q = norm(f), raw = stripDia(f.trim());
    var items = P.surahs.filter(function (s) {
      if (!q && !raw) return true;
      if (q && (String(s.number) === q || norm(s.englishName).indexOf(q) > -1 || norm(s.englishNameTranslation).indexOf(q) > -1)) return true;
      return !!raw && stripDia(s.name).indexOf(raw) > -1;
    });
    box.innerHTML = items.length ? items.map(function (s) {
      return '<button class="list-item" style="margin-bottom:8px" data-a="surah" data-s="' + s.number + '">' +
        '<span class="num">' + s.number + '</span>' +
        '<span class="grow">' + esc(s.englishName) +
        '<div class="muted small">' + s.numberOfAyahs + ' oyat · ' + (s.revelationType === 'Meccan' ? 'Makkiy' : 'Madaniy') + '</div></span>' +
        '<span class="arabic" style="font-size:20px;line-height:1.4">' + esc(s.name) + '</span></button>';
    }).join('') : '<div class="empty">Sura topilmadi</div>';
  }

  function showJuzList() {
    if (!P) return;
    P.mode = 'juzlist'; R = null; stopAudio(); unwatch();
    var h = '<div class="muted small">Pora tanlang. Matn va tarjima ochilganda yuklanadi.</div>';
    for (var j = 1; j <= 30; j++) {
      h += '<button class="list-item" style="margin-bottom:8px" data-a="juz" data-j="' + j + '"><span class="num">' + j +
        '</span><span class="grow">' + j + '-pora</span><span class="muted">›</span></button>';
    }
    P.el.innerHTML = h;
  }

  function showReciters() {
    if (!P) return;
    P.mode = 'reciters';
    setupQueue(7, function (i) {
      return urlMap('surah', 1, getReciter().id).then(function (m) { return m[i + 1]; });
    }, null, function (i) { return 'Al-Fotiha · ' + (i + 1) + '-oyat'; });
    var cur = getReciter().id;
    var h = '<div class="muted small">Tanlangan qori Qur\u2019on o\u2018qish oynasida ishlatiladi. Tinglash tugmasi Al-Fotiha surasini ijro etadi.</div>';
    RECITERS.forEach(function (r) {
      var on = r.id === cur;
      h += '<div class="card"><div class="row between"><div class="grow"><b>' + esc(r.name) + '</b>' +
        '<div class="arabic" style="font-size:20px;line-height:1.6">' + esc(r.ar) + '</div></div>' +
        (on ? '<span class="chip">Tanlangan</span>' : '') + '</div>' +
        '<div class="row" style="margin-top:10px;gap:8px">' +
        '<button class="btn sm ' + (on ? 'ghost' : '') + '" data-a="recpick" data-id="' + r.id + '">' + (on ? '✓ Tanlangan' : 'Tanlash') + '</button>' +
        '<button class="btn sm ghost" data-a="recplay" data-id="' + r.id + '">▶ Tinglash</button></div></div>';
    });
    h += '<div class="src">Audio manbasi: Al Quran Cloud / Islamic Network.</div>' + playerHTML();
    P.el.innerHTML = h;
    setBar();
  }

  /* ---------- O'QISH OYNASI ---------- */
  function openReader(kind, n, target, backLabel) {
    if (!P) return;
    stopAudio(); unwatch();
    var el = P.el;
    P.mode = 'reader'; P.backLabel = backLabel;
    P.retry = function () { openReader(kind, n, target, backLabel); };
    el.innerHTML = T.loaderHTML;
    loadText(kind, n).then(function (data) {
      if (!P || P.el !== el) return;
      var sample = data.ayahs.slice(0, 3).map(function (a) { return a.tr; }).join('');
      R = {
        data: data,
        cyr: /[\u0400-\u04FF]/.test(sample),
        lat: T.store.get('quran:lat', true) !== false,
        fs: T.store.get('quran:fs', 26)
      };
      drawReader(target);
    }).catch(function () {
      if (!P || P.el !== el) return;
      el.innerHTML = '<button class="btn ghost sm" data-a="back">‹ ' + esc(backLabel) + '</button>' +
        T.errorHTML('Matnni yuklab bo\u2018lmadi. Internetni tekshiring.', 'qRetry');
    });
  }

  function trText(a) {
    if (!a.tr) return '';
    return (R.cyr && R.lat) ? lat(a.tr) : a.tr;
  }

  function drawReader(target) {
    var el = P.el, d = R.data, ayahs = d.ayahs, h = '';
    var isS = d.kind === 'surah';

    h += '<div class="row between"><button class="btn ghost sm" data-a="back">‹ ' + esc(P.backLabel) + '</button>' +
      '<span class="row" style="gap:6px"><button class="icon-btn" data-a="fsm">A−</button><button class="icon-btn" data-a="fsp">A+</button>' +
      (R.cyr ? '<button class="icon-btn" id="qScript" data-a="script">' + (R.lat ? 'Кир' : 'Lot') + '</button>' : '') + '</span></div>';

    h += '<div class="card glass" style="text-align:center">';
    if (isS) {
      h += '<div class="arabic" style="text-align:center;font-size:32px;line-height:1.8">' + esc(d.info.name) + '</div>' +
        '<div style="font-weight:700">' + esc(d.info.englishName) + '</div>' +
        '<div class="muted small">' + d.info.numberOfAyahs + ' oyat · ' + (d.info.revelationType === 'Meccan' ? 'Makkiy' : 'Madaniy') + '</div>';
    } else {
      h += '<div style="font-weight:700;font-size:20px">' + d.n + '-pora</div>' +
        '<div class="muted small">' + ayahs.length + ' oyat</div>';
    }
    h += '<div class="muted small" style="margin:8px 0 4px">Qori</div><select data-set="rec">' +
      RECITERS.map(function (r) {
        return '<option value="' + r.id + '"' + (r.id === getReciter().id ? ' selected' : '') + '>' + esc(r.name) + '</option>';
      }).join('') + '</select></div>';

    var src = 'Arabcha matn: quran-uthmani (api.alquran.cloud). ';
    if (d.source) src += 'Tarjima manbasi: ' + esc(d.source.englishName || d.source.name || TR_ED) + ' (' + esc(d.source.identifier || TR_ED) + ').';
    else src += 'O\u2018zbekcha tarjima hozir yuklanmadi, faqat arabcha matn ko\u2018rsatilmoqda.';
    if (R.cyr) src += ' Lotin yozuvi avtomatik o\u2018girilgan, taxminiy.';
    h += '<div class="src" id="qSrc">' + src + '</div>';

    h += '<div id="qRoot" style="--ar:' + R.fs + 'px;display:flex;flex-direction:column;gap:12px">';
    ayahs.forEach(function (a, i) {
      if (isS ? i === 0 : a.n === 1) {
        if (!isS) h += '<div class="card glass" style="text-align:center"><b>' + esc(a.sn) + '</b> <span class="arabic" style="font-size:22px">' + esc(a.sa) + '</span></div>';
        if (a.bismText) h += '<div class="arabic" style="text-align:center;font-size:var(--ar);padding:6px 0">' + esc(a.bismText) + '</div>';
      }
      h += '<div class="ayah" style="scroll-margin-top:72px" data-i="' + i + '" data-s="' + a.s + '" data-n="' + a.n + '" data-sn="' + esc(a.sn) + '">' +
        '<div class="row between"><span class="num">' + a.n + '</span><span class="row" style="gap:6px">' +
        '<button class="icon-btn" data-a="play" data-i="' + i + '">▶</button>' +
        '<button class="icon-btn' + (isBm(a.s, a.n) ? ' on' : '') + '" data-a="bm" data-i="' + i + '">' + (isBm(a.s, a.n) ? '★' : '☆') + '</button>' +
        '<button class="icon-btn" data-a="share" data-i="' + i + '">↗</button></span></div>' +
        '<div class="arabic" style="font-size:var(--ar)">' + esc(a.ar) + '</div>' +
        (a.tr ? '<div class="meaning tr" data-i="' + i + '" style="color:var(--text)">' + esc(trText(a)) + '</div>' : '') +
        '</div>';
    });
    h += '</div>' + playerHTML();
    el.innerHTML = h;

    setupQueue(ayahs.length, function (i) {
      return urlMap(d.kind, d.n, getReciter().id).then(function (m) { return m[ayahs[i].g]; });
    }, function (i) {
      T.$$('.ayah.playing', el).forEach(function (x) { x.classList.remove('playing'); });
      if (i < 0) return;
      var t = el.querySelector('.ayah[data-i="' + i + '"]');
      if (t) { t.classList.add('playing'); try { t.scrollIntoView({ block: 'center', behavior: 'smooth' }); } catch (e) {} }
    }, function (i) { return ayahs[i].sn + ' · ' + ayahs[i].n + '-oyat'; });

    window.scrollTo(0, 0);
    if (target) {
      var t = el.querySelector('.ayah[data-s="' + target.s + '"][data-n="' + target.n + '"]');
      if (t) setTimeout(function () { t.scrollIntoView({ block: 'start' }); }, 60);
    }
    setTimeout(function () { if (P && P.mode === 'reader') watch(); }, 500);
  }

  /* ---------- OXIRGI O'QILGAN JOY ---------- */
  function watch() {
    unwatch();
    if (!('IntersectionObserver' in window) || !P) return;
    obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var t = en.target;
        pending = { s: +t.getAttribute('data-s'), n: +t.getAttribute('data-n'), sn: t.getAttribute('data-sn') };
        clearTimeout(saveTimer);
        saveTimer = setTimeout(flush, 900);
      });
    }, { rootMargin: '0px 0px -65% 0px', threshold: 0 });
    T.$$('.ayah', P.el).forEach(function (x) { obs.observe(x); });
  }
  function unwatch() { if (obs) { obs.disconnect(); obs = null; } }
  function flush() {
    clearTimeout(saveTimer);
    if (pending && pending.s) T.store.set('quran:last', pending);
    pending = null;
  }

  /* ---------- HODISALAR ---------- */
  function onClick(e) {
    if (!P) return;
    if (e.target.id === 'qRetry') { if (P.mode === 'reader' && P.retry) P.retry(); else if (P.kind === 'quran') showList(P.tab); return; }
    var b = e.target.closest('[data-a]');
    if (!b) return;
    var a = b.getAttribute('data-a');
    var i = +b.getAttribute('data-i');

    if (a === 'tab') { showList(b.getAttribute('data-t')); }
    else if (a === 'surah') { openReader('surah', +b.getAttribute('data-s'), null, 'Suralar'); }
    else if (a === 'juz') { openReader('juz', +b.getAttribute('data-j'), null, 'Porallar'.replace('Porallar', 'Poralar')); }
    else if (a === 'cont') { var l = T.store.get('quran:last', null); if (l) openReader('surah', l.s, { s: l.s, n: l.n }, 'Suralar'); }
    else if (a === 'bmopen') { var s = +b.getAttribute('data-s'), n = +b.getAttribute('data-n'); openReader('surah', s, { s: s, n: n }, 'Belgilanganlar'); }
    else if (a === 'bmdel') {
      var s2 = +b.getAttribute('data-s'), n2 = +b.getAttribute('data-n');
      T.store.set('quran:bm', bmList().filter(function (x) { return !(x.s === s2 && x.n === n2); }));
      showList('bm');
    }
    else if (a === 'back') {
      flush();
      if (P.kind === 'juz') showJuzList();
      else showList(P.backLabel === 'Belgilanganlar' ? 'bm' : 'surahs');
    }
    else if (a === 'fsm' || a === 'fsp') {
      if (!R) return;
      R.fs = Math.max(20, Math.min(44, R.fs + (a === 'fsp' ? 2 : -2)));
      T.store.set('quran:fs', R.fs);
      var root = document.getElementById('qRoot');
      if (root) root.style.setProperty('--ar', R.fs + 'px');
    }
    else if (a === 'script') {
      if (!R) return;
      R.lat = !R.lat;
      T.store.set('quran:lat', R.lat);
      b.textContent = R.lat ? 'Кир' : 'Lot';
      T.$$('.tr', P.el).forEach(function (x) {
        x.textContent = trText(R.data.ayahs[+x.getAttribute('data-i')]);
      });
    }
    else if (a === 'play') {
      if (Q.i === i && Q.audio && !Q.audio.paused) Q.audio.pause();
      else if (Q.i === i && Q.audio && Q.audio.paused && Q.audio.src && Q.audio.src.indexOf('data:') !== 0) {
        var p = Q.audio.play(); if (p && p.catch) p.catch(function () {});
      } else { unlock(); playAt(i); }
    }
    else if (a === 'bm') {
      var ay = R.data.ayahs[i];
      var on = toggleBm(ay);
      b.textContent = on ? '★' : '☆';
      b.classList.toggle('on', on);
      T.tg.haptic('light');
      T.toast(on ? 'Belgilandi' : 'Belgi olib tashlandi');
    }
    else if (a === 'share') {
      var ay2 = R.data.ayahs[i];
      T.tg.share(ay2.ar + '\n\n' + trText(ay2) + '\n\n— ' + ay2.sn + ' ' + ay2.s + ':' + ay2.n);
    }
    else if (a === 'prev') { unlock(); playAt(Q.i > 0 ? Q.i - 1 : 0); }
    else if (a === 'next') { unlock(); if (Q.i + 1 < Q.n) playAt(Q.i + 1); }
    else if (a === 'toggle') { unlock(); toggle(); }
    else if (a === 'recpick') {
      T.store.set('quran:reciter', b.getAttribute('data-id'));
      stopAudio();
      showReciters();
      T.toast('Qori tanlandi');
    }
    else if (a === 'recplay') {
      T.store.set('quran:reciter', b.getAttribute('data-id'));
      unlock();
      showReciters();
      unlock();
      playAt(0);
    }
  }

  function onInput(e) {
    if (e.target.id === 'qSearch') fillList(e.target.value);
  }
  function onChange(e) {
    if (e.target.getAttribute('data-set') === 'rec') {
      T.store.set('quran:reciter', e.target.value);
      stopAudio();
      T.toast('Qori almashtirildi');
    }
  }

  /* ---------- BO'LIMLARNI RO'YXATGA OLISH ---------- */
  function mount(kind, start) {
    return function (el) {
      P = { el: el, kind: kind, tab: 'surahs', mode: '' };
      el.onclick = onClick;
      el.oninput = onInput;
      el.onchange = onChange;
      start();
    };
  }
  function leave() {
    flush(); unwatch(); stopAudio();
    if (P && P.el) { P.el.onclick = null; P.el.oninput = null; P.el.onchange = null; }
    P = null; R = null;
  }

  T.sections.quran = { title: 'Qur\u2019oni Karim', icon: '📖', render: mount('quran', function () { showList('surahs'); }), leave: leave };
  T.sections.juz = { title: 'Qur\u2019onning 30 porasi', icon: '📚', render: mount('juz', showJuzList), leave: leave };
  T.sections.reciters = { title: 'Qur\u2019on qorilari', icon: '🎙️', render: mount('reciters', showReciters), leave: leave };
})();
