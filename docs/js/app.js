/* TAQVO PRO MAX - app.js (bosh sahifa va navigatsiya) */
(function () {
  'use strict';
  var T = window.TAQVO;

  // Aynan 17 ta bo'lim, berilgan tartibda
  var SECTIONS = [
    { id: 'quran',    icon: '📖', title: 'Qur\'oni Karim', wide: true },
    { id: 'videos',   icon: '🎬', title: 'Islomiy videolar' },
    { id: 'tasbeeh',  icon: '📿', title: 'Tasbeh' },
    { id: 'adhkar',   icon: '🌅', title: 'Tonggi va kechgi zikrlar' },
    { id: 'quiz',     icon: '🧠', title: 'Siyrat viktorinasi' },
    { id: 'farz',     icon: '🕋', title: 'Farz amallari' },
    { id: 'qa',       icon: '💬', title: 'Islomiy savol-javob' },
    { id: 'hadith',   icon: '📜', title: 'Sahih hadislar' },
    { id: 'dua',      icon: '🤲', title: 'Duolar' },
    { id: 'reciters', icon: '🎙️', title: 'Qur\'on qorilari' },
    { id: 'juz',      icon: '📚', title: 'Qur\'onning 30 porasi' },
    { id: 'names',    icon: '✨', title: 'Allohning 99 go\'zal ismi' },
    { id: 'ranking',  icon: '🏆', title: 'Foydalanuvchilar reytingi' },
    { id: 'prayer',   icon: '🕌', title: 'Namoz vaqtlari' },
    { id: 'sirah',    icon: '🌙', title: 'Payg\'ambarimiz ﷺ siyratlari' },
    { id: 'fiqh',     icon: '⚖️', title: 'Fiqh' },
    { id: 'ai',       icon: '🤖', title: 'TAQVO AI' }
  ];

  var byId = {};
  SECTIONS.forEach(function (s) { byId[s.id] = s; });

  var S = { current: null, pushed: false, scrollY: 0 };

  function $(id) { return document.getElementById(id); }

  /* ---------- SALOMLASHISH VA SANA ---------- */
  function greetingText() {
    var h = new Date().getHours();
    var part = h < 5 ? 'Xayrli tun' : h < 11 ? 'Xayrli tong' : h < 17 ? 'Xayrli kun' : h < 21 ? 'Xayrli kech' : 'Xayrli tun';
    var u = T.tg.user;
    var name = u && u.first_name ? u.first_name : '';
    return 'Assalomu alaykum' + (name ? ', ' + name : '') + ' · ' + part;
  }

  function updateHeader() {
    var g = $('greeting');
    if (g) g.textContent = greetingText();
    var d = $('dateG');
    if (d) d.textContent = T.formatDate(new Date());
  }

  /* ---------- BOSH SAHIFA: 17 BO'LIM ---------- */
  function buildGrid() {
    var grid = $('sectionGrid');
    if (!grid) return;
    grid.innerHTML = SECTIONS.map(function (s) {
      var ready = !!T.sections[s.id];
      return '<button class="tile' + (s.wide ? ' wide' : '') + '" data-sec="' + s.id + '">' +
        '<span class="ic">' + s.icon + '</span>' +
        '<span class="tt">' + T.esc(s.title) + '</span>' +
        (ready ? '' : '<span class="chip" style="align-self:flex-start">Tez orada</span>') +
        '</button>';
    }).join('');
  }

  /* ---------- TAYYOR BO'LMAGAN BO'LIM ---------- */
  function renderPlaceholder(el, sec) {
    el.innerHTML =
      '<div class="card" style="text-align:center;padding:26px 16px">' +
      '<div style="font-size:46px">' + sec.icon + '</div>' +
      '<h3 style="margin:10px 0 6px">' + T.esc(sec.title) + '</h3>' +
      '<p class="muted" style="font-size:14px;line-height:1.6;margin:0 0 16px">' +
      'Bu bo\'lim ustida ishlanmoqda va keyingi yangilanishda qo\'shiladi. ' +
      'Yangiliklardan xabardor bo\'lish uchun kanalimizga obuna bo\'ling.</p>' +
      '<button class="btn" data-open-channel="1">Kanalga o\'tish</button></div>';
  }

  /* ---------- SAHIFALAR ---------- */
  function leaveCurrent() {
    var cur = S.current && T.sections[S.current];
    if (cur && typeof cur.leave === 'function') {
      try { cur.leave(); } catch (e) {}
    }
    S.current = null;
  }

  function showHome() {
    leaveCurrent();
    $('page').classList.remove('active');
    $('home').classList.add('active');
    $('pageBody').innerHTML = '';
    T.tg.hideBack();
    updateHeader();
    window.scrollTo(0, S.scrollY || 0);
  }

  function showSection(id) {
    var sec = byId[id];
    if (!sec) { showHome(); return; }
    if (S.current === id) return;
    if (!S.current) S.scrollY = window.pageYOffset || 0;
    leaveCurrent();

    $('home').classList.remove('active');
    $('page').classList.add('active');
    $('pageTitle').textContent = sec.title;
    var body = $('pageBody');
    body.innerHTML = '';
    body.removeAttribute('data-sec');
    window.scrollTo(0, 0);
    S.current = id;
    T.tg.showBack(goBack);

    var mod = T.sections[id];
    try {
      if (mod && typeof mod.render === 'function') mod.render(body);
      else renderPlaceholder(body, sec);
    } catch (err) {
      body.innerHTML = T.errorHTML('Bo\'limni ochishda xatolik yuz berdi');
      if (window.console) console.error(err);
    }
  }

  function openSection(id) {
    if (!byId[id]) return;
    S.pushed = true;
    location.hash = id;
  }

  function goBack() {
    if (S.pushed) history.back();
    else location.hash = '';
  }

  function route() {
    var id = (location.hash || '').replace('#', '');
    if (id && byId[id]) showSection(id);
    else showHome();
  }

  /* ---------- BOSHLASH ---------- */
  function init() {
    T.tg.init();
    updateHeader();
    buildGrid();

    if (T.prayer && T.prayer.init) T.prayer.init();

    $('sectionGrid').addEventListener('click', function (e) {
      var b = e.target.closest('[data-sec]');
      if (!b) return;
      T.tg.haptic('light');
      openSection(b.getAttribute('data-sec'));
    });

    $('backBtn').addEventListener('click', goBack);

    $('pageBody').addEventListener('click', function (e) {
      if (e.target.closest('[data-open-channel]')) T.tg.openLink(T.config.CHANNEL);
    });

    window.addEventListener('hashchange', route);

    // Sahifa ochilganda sana to'g'ri bo'lishi uchun
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) updateHeader();
    });

    route();
  }

  T.app = { open: openSection, back: goBack, sections: SECTIONS };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
