/* TAQVO PRO MAX - api.js (umumiy poydevor) */
(function () {
  'use strict';

  var TAQVO = (window.TAQVO = window.TAQVO || {});
  TAQVO.sections = {}; // har bir modul o'zini shu yerga ro'yxatdan o'tkazadi

  /* ---------- SOZLAMALAR ---------- */
  TAQVO.config = {
    // Backend (Render) manzili. Backend tayyor bo'lgach shu yerga yozing.
    // Masalan: 'https://taqvo-api.onrender.com'. Bo'sh bo'lsa, ilova offline rejimda ishlaydi.
    API_BASE: '',
    ALADHAN: 'https://api.aladhan.com/v1',
    QURAN: 'https://api.alquran.cloud/v1',
    AUDIO_CDN: 'https://cdn.islamic.network/quran/audio',
    CHANNEL: 'https://t.me/hakiymqalb'
  };

  /* ---------- YORDAMCHI FUNKSIYALAR ---------- */
  TAQVO.esc = function (s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  };
  TAQVO.pad = function (n) { return n < 10 ? '0' + n : String(n); };
  TAQVO.debounce = function (fn, ms) {
    var t;
    return function () {
      var a = arguments, c = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(c, a); }, ms || 250);
    };
  };
  TAQVO.$ = function (sel, root) { return (root || document).querySelector(sel); };
  TAQVO.$$ = function (sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); };

  /* ---------- SAQLASH (localStorage) ---------- */
  var PREFIX = 'taqvo:';
  TAQVO.store = {
    get: function (key, def) {
      try {
        var v = localStorage.getItem(PREFIX + key);
        return v === null ? def : JSON.parse(v);
      } catch (e) { return def; }
    },
    set: function (key, val) {
      try { localStorage.setItem(PREFIX + key, JSON.stringify(val)); return true; }
      catch (e) { return false; }
    },
    remove: function (key) {
      try { localStorage.removeItem(PREFIX + key); } catch (e) {}
    }
  };

  /* ---------- XABAR (toast) ---------- */
  var toastTimer;
  TAQVO.toast = function (msg) {
    var el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.classList.remove('show'); }, 2400);
  };

  /* ---------- TELEGRAM ---------- */
  var wa = (window.Telegram && window.Telegram.WebApp) || null;
  TAQVO.tg = {
    app: wa,
    isTelegram: !!(wa && wa.initData),
    initData: wa ? wa.initData || '' : '',
    user: wa && wa.initDataUnsafe ? wa.initDataUnsafe.user || null : null, // faqat ko'rsatish uchun
    init: function () {
      if (!wa) return;
      try {
        wa.ready();
        wa.expand();
        if (wa.setHeaderColor) wa.setHeaderColor('#08090D');
        if (wa.setBackgroundColor) wa.setBackgroundColor('#08090D');
        if (wa.disableVerticalSwipes) wa.disableVerticalSwipes();
      } catch (e) {}
    },
    haptic: function (kind) {
      try {
        var h = wa && wa.HapticFeedback;
        if (h) {
          if (kind === 'success' || kind === 'error' || kind === 'warning') h.notificationOccurred(kind);
          else h.impactOccurred(kind || 'light');
          return;
        }
      } catch (e) {}
      if (navigator.vibrate) { try { navigator.vibrate(kind === 'heavy' ? 40 : 15); } catch (e2) {} }
    },
    showBack: function (cb) {
      if (!wa || !wa.BackButton) return;
      try {
        if (TAQVO.tg._backCb) wa.BackButton.offClick(TAQVO.tg._backCb);
        TAQVO.tg._backCb = cb;
        wa.BackButton.onClick(cb);
        wa.BackButton.show();
      } catch (e) {}
    },
    hideBack: function () {
      if (!wa || !wa.BackButton) return;
      try {
        if (TAQVO.tg._backCb) wa.BackButton.offClick(TAQVO.tg._backCb);
        TAQVO.tg._backCb = null;
        wa.BackButton.hide();
      } catch (e) {}
    },
    openLink: function (url) {
      try {
        if (wa && url.indexOf('https://t.me/') === 0 && wa.openTelegramLink) { wa.openTelegramLink(url); return; }
        if (wa && wa.openLink) { wa.openLink(url); return; }
      } catch (e) {}
      window.open(url, '_blank');
    },
    share: function (text) {
      var url = 'https://t.me/share/url?url=' + encodeURIComponent(TAQVO.config.CHANNEL) +
        '&text=' + encodeURIComponent(text);
      TAQVO.tg.openLink(url);
    }
  };

  /* ---------- TARMOQ ---------- */
  // Vaqt chegarasi bilan JSON olish
  TAQVO.getJSON = function (url, opts) {
    opts = opts || {};
    var timeout = opts.timeout || 12000;
    var retries = opts.retries == null ? 1 : opts.retries;
    function attempt(n) {
      var ctrl = typeof AbortController !== 'undefined' ? new AbortController() : null;
      var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, timeout);
      return fetch(url, ctrl ? { signal: ctrl.signal } : undefined)
        .then(function (r) {
          clearTimeout(timer);
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .catch(function (err) {
          clearTimeout(timer);
          if (n < retries) return attempt(n + 1);
          throw err;
        });
    }
    return attempt(0);
  };

  // Keshli JSON (offline uchun foydali). ttl - millisekund.
  TAQVO.cachedJSON = function (url, ttl, opts) {
    var key = 'cache:' + url;
    var hit = TAQVO.store.get(key, null);
    var now = Date.now();
    if (hit && hit.t && now - hit.t < ttl) return Promise.resolve(hit.d);
    return TAQVO.getJSON(url, opts).then(function (d) {
      var ok = TAQVO.store.set(key, { t: now, d: d });
      if (!ok) cleanCache(); // joy yetmasa eski keshni tozalaymiz
      return d;
    }).catch(function (err) {
      if (hit && hit.d) return hit.d; // internet yo'q bo'lsa eski nusxa
      throw err;
    });
  };

  function cleanCache() {
    try {
      var keys = [];
      for (var i = 0; i < localStorage.length; i++) {
        var k = localStorage.key(i);
        if (k && k.indexOf(PREFIX + 'cache:') === 0) keys.push(k);
      }
      keys.forEach(function (k) { localStorage.removeItem(k); });
    } catch (e) {}
  }

  /* ---------- BACKEND (Render) ---------- */
  // Telegram initData sarlavhada yuboriladi, backend uni tekshiradi.
  // API_BASE bo'sh bo'lsa null qaytaradi (ilova offline ishlaydi).
  TAQVO.backend = {
    enabled: function () { return !!TAQVO.config.API_BASE; },
    request: function (path, options) {
      if (!TAQVO.config.API_BASE) return Promise.resolve(null);
      options = options || {};
      var headers = { 'Content-Type': 'application/json' };
      if (TAQVO.tg.initData) headers['X-Telegram-Init-Data'] = TAQVO.tg.initData;
      return fetch(TAQVO.config.API_BASE + path, {
        method: options.method || 'GET',
        headers: headers,
        body: options.body ? JSON.stringify(options.body) : undefined
      }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      });
    }
  };

  /* ---------- HIJRIY / MILODIY SANA ---------- */
  var MONTHS_UZ = ['yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'];
  var DAYS_UZ = ['Yakshanba', 'Dushanba', 'Seshanba', 'Chorshanba', 'Payshanba', 'Juma', 'Shanba'];
  TAQVO.formatDate = function (d) {
    d = d || new Date();
    return DAYS_UZ[d.getDay()] + ', ' + d.getDate() + ' ' + MONTHS_UZ[d.getMonth()] + ' ' + d.getFullYear();
  };

  /* ---------- UMUMIY HTML QISMLAR ---------- */
  TAQVO.loaderHTML = '<div class="loader"></div>';
  TAQVO.errorHTML = function (msg, retryId) {
    return '<div class="empty">⚠️ ' + TAQVO.esc(msg) +
      (retryId ? '<br><br><button class="btn sm" id="' + retryId + '">Qayta urinish</button>' : '') + '</div>';
  };
})();
