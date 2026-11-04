/* TAQVO PRO MAX — Farz amallar, Siyrat, Fiqh (umumiy ma'lumot, fatvo emas).
   Fiqh qismi asosan Hanafiy mazhabi bo'yicha; mazhablar farqi aniq ko'rsatilgan joylarda yozilgan.
   Matnlarni nashrdan oldin ishonchli olim yoki muftiylik bilan tekshirtiring. */
(() => {
  const el = (t, c, x) => { const e = document.createElement(t); if (c) e.className = c; if (x != null) e.textContent = x; return e; };
  const NOTE = 'Bu umumiy ma’lumot, fatvo emas. Murakkab masalalarda ishonchli olim yoki muftiylikka murojaat qiling.';
  function topics(root, data, cur, redraw, title, status) {
    root.textContent = '';
    const tabs = el('div', 'q-tabs');
    data.forEach((d) => { const b = el('button', 'zk-chip' + (d.k === cur ? ' act' : ''), d.k); b.onclick = () => redraw(d.k); tabs.appendChild(b); });
    root.appendChild(tabs);
    const d = data.find((x) => x.k === cur);
    d.items.forEach((it) => {
      const c = el('div', 'zk-card'); c.style.marginBottom = '10px'; c.appendChild(el('h3', null, it[0]));
      it[1].forEach((line) => c.appendChild(el('p', 'zk-uz', line)));
      c.appendChild(el('p', 'zk-src', 'Manba: ' + it[2])); root.appendChild(c);
    });
    root.appendChild(el('p', 'zk-src', NOTE));
    return { title, status };
  }

  // ---------------- FARZ AMALLAR
  const FARZ = [
    { k: 'Islom ustunlari', items: [['Islom besh narsa ustiga qurilgan', ['1. Allohdan o‘zga iloh yo‘qligiga va Muhammad ﷺ Allohning elchisi ekanligiga guvohlik berish.', '2. Namozni to‘kis ado etish.', '3. Zakot berish.', '4. Ramazon ro‘zasini tutish.', '5. Qurbi yetgan kishi uchun Baytullohni haj qilish.'], 'Buxoriy 8, Muslim 16']] },
    { k: 'Iymon rukunlari', items: [['Iymonning oltita asosi', ['Allohga, Uning farishtalariga, kitoblariga, payg‘ambarlariga, oxirat kuniga va yaxshi-yomon taqdirning Alloh tomonidan ekaniga iymon keltirish.'], 'Muslim 8']] },
    { k: 'Namoz', items: [['Kuniga besh vaqt namoz farz', ['Bomdod: 2 rakat. Peshin: 4. Asr: 4. Shom: 3. Xufton: 4 (farz rakatlar).', 'Hanafiy mazhabida Xufton orqasidagi vitr namozi vojib.'], 'Qur’on 4:103; Buxoriy 8, Muslim 16']] },
    { k: 'Zakot', items: [['Zakot kimga va qancha', ['Nisobga yetgan molga bir yil to‘lgach, umumiy boylikning 2,5 foizi beriladi.', 'Nisob taxminan 85 g oltin yoki 595 g kumush qiymatiga teng. Naqd pul uchun qaysi biri asos bo‘lishi mazhab va muftiylik fatvosiga bog‘liq, shuning uchun hisoblashda muftiylikdan so‘rang.'], 'Qur’on 9:60; Buxoriy 1454']] },
    { k: 'Ro‘za', items: [['Ramazon ro‘zasi', ['Ramazon oyida tong otishidan quyosh botguncha ro‘za tutiladi. Niyat qilish shart.', 'Ataylab yeb-ichish va jimo‘ ro‘zani buzadi.'], 'Qur’on 2:183-187']] },
    { k: 'Haj', items: [['Haj', ['Umrda bir marta, jismoniy va moliyaviy qurbi yetgan musulmonga farz.', 'Hanafiyda haj farzlari: ihrom, Arafotda turish va tavofi ziyorat.'], 'Qur’on 3:97; Buxoriy 8']] },
  ];
  // ---------------- SIYRAT
  const SIYRAT = [
    ['570 (taxminan)', 'Tug‘ilish', 'Makkada, Fil yili Rabi’ul-avval oyida tug‘ildilar. Otalari Abdulloh tug‘ilishlaridan oldin, onalari Omina taxminan olti yoshlarida vafot etdi. Keyin bobolari Abdulmuttalib, so‘ng amakilari Abu Tolib tarbiyalagan.'],
    ['595 (taxminan)', 'Xadichaga uylanish', '25 yoshda Xadicha roziyallohu anho bilan turmush qurdilar.'],
    ['610', 'Birinchi vahiy', '40 yoshda Hiro g‘orida Jabroil alayhissalom kelib, “Iqra” suralari (96:1-5) ning dastlabki oyatlarini keltirdi.'],
    ['613 (taxminan)', 'Ochiq da’vat', 'Uch yillik yashirin da’vatdan keyin Islom ochiq e’lon qilindi.'],
    ['615', 'Habashistonga hijrat', 'Quraysh zulmidan qochib, bir guruh sahobalar Habashistonga ketdi.'],
    ['619', 'Qayg‘u yili', 'Xadicha roziyallohu anho va amakilari Abu Tolib vafot etdi.'],
    ['621 (taxminan)', 'Isro va Me’roj', 'Makkadan Qudsga, u yerdan osmonlarga safar. Besh vaqt namoz farz bo‘lgan.'],
    ['622 · 1-hijriy', 'Madinaga hijrat', 'Rasululloh ﷺ Abu Bakr bilan Madinaga hijrat qildilar. Hijriy yil shu yildan hisoblanadi.'],
    ['624 · 2-hijriy', 'Badr g‘azoti', 'Ramazon oyida musulmonlar sonining oz bo‘lishiga qaramay g‘alaba qozondi.'],
    ['625 · 3-hijriy', 'Uhud g‘azoti', 'O‘qchilar o‘z o‘rnini tark etgach, jang musulmonlar uchun og‘ir kechdi.'],
    ['627 · 5-hijriy', 'Xandaq g‘azoti', 'Madinaga hujum qilgan ittifoqchi qo‘shinga qarshi xandaq qazildi.'],
    ['628 · 6-hijriy', 'Hudaybiya sulhi', 'Makka mushriklari bilan sulh tuzildi, Islom tarqalishiga keng yo‘l ochildi.'],
    ['630 · 8-hijriy', 'Makka fathi', 'Makka deyarli to‘qnashuvsiz fath etildi, Ka’ba butlardan tozalandi.'],
    ['632 · 10-hijriy', 'Vido haji', 'Arafotda tarixiy xutba irod qildilar.'],
    ['632 · 11-hijriy', 'Vafot', 'Rabi’ul-avval oyida 63 yoshda Madinada vafot etdilar, hujrai saodatlariga dafn qilindilar.'],
  ];
  function siyrat(root) {
    root.textContent = '';
    root.appendChild(el('p', 'zk-note', 'Muhim voqealar xronologiyasi. Hijratgacha bo‘lgan sanalar taxminiy.'));
    SIYRAT.forEach((s) => { const c = el('div', 'zk-card'); c.style.marginBottom = '10px'; c.appendChild(el('h3', null, s[0] + ' · ' + s[1])); c.appendChild(el('p', 'zk-uz', s[2])); root.appendChild(c); });
    root.appendChild(el('p', 'zk-src', 'Umumiy ma’lumot. Batafsil: “Ar-Rahiyqul-maxtum” va boshqa ishonchli siyrat kitoblari.'));
    return { title: 'Siyrat', status: SIYRAT.length + ' ta voqea' };
  }
  // ---------------- FIQH
  const FIQH = [
    { k: 'Tahorat', items: [
      ['Tahoratning farzlari (Hanafiy)', ['1. Yuzni yuvish.', '2. Ikki qo‘lni tirsaklari bilan yuvish.', '3. Boshning to‘rtdan biriga mas’h tortish.', '4. Ikki oyoqni to‘piqlari bilan yuvish.'], 'Qur’on 5:6'],
      ['Tahoratni buzadigan holatlar (Hanafiy)', ['Old yoki orqa yo‘ldan biror narsa chiqishi; badandan qon yoki yiring oqib chiqishi; og‘iz to‘la qusish; yonboshlab yoki suyanib uxlash; hushdan ketish; namozda qah-qah urib kulish.'], 'Hanafiy fiqh kitoblari']] },
    { k: 'G‘usl', items: [
      ['G‘uslning farzlari (Hanafiy)', ['1. Og‘izni chayish.', '2. Burunni chayish.', '3. Butun badanga suv yetkazish.'], 'Qur’on 5:6'],
      ['G‘usl qachon farz', ['Janobatdan keyin va hayz hamda nifos tugagach.'], 'Qur’on 5:6; 2:222']] },
    { k: 'Namoz', items: [
      ['Namozning shartlari', ['Hadas va najosatdan pok bo‘lish, avratni yopish, qiblaga yuzlanish, vaqt kirishi va niyat.'], 'Hanafiy fiqh kitoblari'],
      ['Namozning farzlari (Hanafiy)', ['1. Takbiri tahrima. 2. Qiyom. 3. Qiroat. 4. Ruku’. 5. Sajda. 6. Oxirgi qa’da.'], 'Hanafiy fiqh kitoblari']] },
    { k: 'Mazhablar farqi', items: [
      ['Tahoratda bosh mas’hi', ['Hanafiy: boshning to‘rtdan biri. Molikiy va Hanbaliy: butun bosh. Shofi’iy: bir qismi.'], 'To‘rt mazhab fiqh kitoblari'],
      ['Ayol terisiga tegish', ['Shofi’iy mazhabida (shahvatsiz ham) tahoratni buzadi. Hanafiy mazhabida shahvatsiz tegish tahoratni buzmaydi.'], 'To‘rt mazhab fiqh kitoblari']] },
    { k: 'Ro‘za, zakot, haj', items: [
      ['Ro‘za', ['Niyat bilan tong otishidan quyosh botguncha yeb-ichishdan va jimo‘dan saqlanish.'], 'Qur’on 2:187'],
      ['Zakot', ['Nisobga yetgan molning 2,5 foizi. Batafsil hisob uchun “Farz amallar” va muftiylikka qarang.'], 'Qur’on 9:60'],
      ['Haj va umra', ['Haj va umra amallari murakkab: ihrom, tavof, sa’y, Arafot. Safardan oldin ishonchli haj yo‘lboshchisidan o‘rganing.'], 'Qur’on 2:196-197; 3:97']] },
  ];
  window.TaqvoSections = window.TaqvoSections || {};
  Object.assign(window.TaqvoSections, {
    farz: (r, k) => { const x = (kk) => topics(r, FARZ, kk, x, 'Farz amallar', '6 ta mavzu'); return x(k || FARZ[0].k); },
    fiqh: (r, k) => { const x = (kk) => topics(r, FIQH, kk, x, 'Fiqh', 'Hanafiy mazhabi'); return x(k || FIQH[0].k); },
    siyrat,
  });
})();
