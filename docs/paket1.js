/* paket1.js — TAQVO tuzatishlari (to'liq fayl) */
(function () {
const SERVER = "https://taqvo-bot-api.onrender.com";
  const app = document.getElementById('app');
  app.style.visibility = 'hidden';
  CFG.API = SERVER;
  let OK = false;

  // Botga mos so'rov: /api/... va initData
  window.api = async function (p, b) {
    const r = await fetch(CFG.API + '/api' + p, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ initData: (tg && tg.initData) || '', ...b })
    });
    return r.json();
  };

  // Obuna tasdiqlanmaguncha hech qaysi bo'lim ochilmaydi
  const _go = window.go;
  window.go = function () { if (!OK) return; return _go.apply(this, arguments); };

  window.boot = async function () {
    nav();
    OK = false;
    if (!(tg && tg.initData)) { gate('tg'); app.style.visibility = 'visible'; return; }
    try {
      const r = await api('/check', {});
      if (r.ok) { OK = true; go('home'); } else gate('sub');
    } catch (e) { gate('net'); }
    app.style.visibility = 'visible';
  };

  // Buzuq arabcha matn tuzatildi
  D.d.forEach(x => { if (x[0] === 'Masjiddan chiqishda') x[2] = 'اللَّهُمَّ إِنِّي أَسْأَلُكَ مِنْ فَضْلِكَ'; });

  // Namoz taymeri to'planib qolmasin
  const _lt = window.lt;
  window.lt = function () { clearInterval(tmr); return _lt(); };

  // Kuniga ball chegarasi
  const _pts = window.pts;
  window.pts = function (n) {
    if (n > 0) {
      const k = 'cap' + new Date().toDateString(), u = S.g(k, 0);
      if (u >= 300) { toast("Bugungi ball limiti to'ldi"); return; }
      n = Math.min(n, 300 - u); S.s(k, u + n);
    }
    _pts(n);
  };

  boot();
})();
