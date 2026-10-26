
"use strict";

/* TAQVO PRO MAX — asosiy interfeys */
const API = "https://taqvo-bot-api.onrender.com";
const $ = id => document.getElementById(id);

const MENU = [
 ["quran","📖","Qur’oni Karim","114 sura"],
 ["recitation","🎧","Qur’on qiroatlari","Qorilar va audio"],
 ["tasbih","📿","Tasbeh","Zikr sanagichi"],
 ["morning","🌅","Tonggi zikrlar","Tonggi zikrlar"],
 ["evening","🌙","Kechki zikrlar","Kechki zikrlar"],
 ["prayer","🕌","Namoz vaqtlari","Shahar bo‘yicha"],
 ["duas","🤲","Sahih duolar","Duolar va ma’nolari"],
 ["hadith","📜","Hadislar","Hadislarni o‘rganish"],
 ["forty","☪️","Qirq farz","O‘rganish"],
 ["duties","🧭","Asosiy burchlar","Diniy bilimlar"],
 ["foundations","🌿","Islom asoslari","Asosiy bilimlar"],
 ["sirah","🕋","Payg‘ambarimiz ﷺ siyratlari","Siyrat bosqichlari"],
 ["quiz","🎯","Siyrat o‘yini","Savollar va ballar"],
 ["ranking","🏆","Reyting","Medallar va natijalar"],
 ["media","🎬","Islomiy kino va multfilmlar","Ishonchli manbalar"],
 ["ai","🤖","TAQVO AI","Savol-javob"],
 ["settings","🔤","Til va sozlamalar","Lotin / Кирилл"]
];

const ZIKR = [
 {a:"سُبْحَانَ اللَّهِ",t:"Subhanalloh",m:"Alloh barcha nuqsonlardan pokdir.",n:33,src:"Sahih Muslim 597"},
 {a:"الْحَمْدُ لِلَّهِ",t:"Alhamdulillah",m:"Barcha hamd Allohgadir.",n:33,src:"Sahih Muslim 597"},
 {a:"اللَّهُ أَكْبَرُ",t:"Allohu akbar",m:"Alloh eng buyukdir.",n:34,src:"Sahih Muslim 597"},
 {a:"أَسْتَغْفِرُ اللَّهَ",t:"Astag‘firulloh",m:"Allohdan mag‘firat so‘rayman.",n:3,src:"Sahih Muslim 591"},
 {a:"لَا إِلَهَ إِلَّا اللَّهُ",t:"La ilaha illalloh",m:"Allohdan boshqa haq iloh yo‘q.",n:100,src:"Sahih Muslim 2691"}
];

const RECITERS = [
 {name:"Mishary Rashid Alafasy",id:"ar.alafasy"},
 {name:"Abdul Basit — Murattal",id:"ar.abdulbasitmurattal"},
 {name:"Abdurrahman As-Sudais",id:"ar.abdurrahmaansudais"},
 {name:"Maher Al Muaiqly",id:"ar.mahermuaiqly"},
 {name:"Saud Al-Shuraim",id:"ar.saoodshuraym"},
 {name:"Hani Ar-Rifai",id:"ar.hanirifai"}
];

let suras = [];
let zikrIndex = 0;
let zikrCount = 0;
let isCyrillic = false;
let quizIndex = 0;
let quizScore = 0;
let quizQuestions = [];

function safe(value) {
 return String(value ?? "").replace(/[&<>"']/g, ch => ({
  "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
 }[ch]));
}

async function getJSON(url, options) {
 const response = await fetch(url, options);
 if (!response.ok) throw new Error("HTTP " + response.status);
 return response.json();
}

/* Menyu */
function renderMenu(filter = "") {
 $("menu").innerHTML = "";
 MENU.filter(item =>
  (item[2] + " " + item[3]).toLowerCase().includes(filter.toLowerCase())
 ).forEach(item => {
  const button = document.createElement("button");
  button.className = "tile";
  button.innerHTML =
   `<span class="emoji">${item[1]}</span><b>${safe(item[2])}</b><small>${safe(item[3])}</small>`;
  button.addEventListener("click", () => openPage(item[0]));
  $("menu").appendChild(button);
 });
}

/* Tanlangan bo‘limdan boshqa bosh sahifa qismlarini yashirish */
function page(title, html) {
 $("pageTitle").textContent = title;
 $("content").innerHTML = html;
 $("page").classList.remove("hidden");
 $("menu").classList.add("hidden");
 $("search").classList.add("hidden");
 $("allHeading").classList.add("hidden");
 document.querySelector(".hero")?.classList.add("hidden");
 document.querySelector(".quick")?.classList.add("hidden");
 document.querySelectorAll(".section-title").forEach(el => el.classList.add("hidden"));
 window.scrollTo({top:0,behavior:"smooth"});
}

function home() {
 $("page").classList.add("hidden");
 $("menu").classList.remove("hidden");
 $("search").classList.remove("hidden");
 $("allHeading").classList.remove("hidden");
 document.querySelector(".hero")?.classList.remove("hidden");
 document.querySelector(".quick")?.classList.remove("hidden");
 document.querySelectorAll(".section-title").forEach(el => el.classList.remove("hidden"));
 window.scrollTo({top:0,behavior:"smooth"});
}
$("back").onclick = home;

/* Qur’oni Karim — suralar ro‘yxati, arabcha matn va tarjima */
async function loadSuras() {
 page("Qur’oni Karim",'<p class="muted">Suralar yuklanmoqda...</p>');
 try {
  const result = await getJSON("https://api.alquran.cloud/v1/surah");
  suras = result.data || [];
  $("content").innerHTML =
   '<input id="surahSearch" placeholder="Sura nomini qidiring"><div id="surahList"></div>';
  const draw = () => {
   const query = $("surahSearch").value.toLowerCase();
   $("surahList").innerHTML = "";
   suras.filter(s =>
    (s.englishName + " " + s.name + " " + s.number).toLowerCase().includes(query)
   ).forEach(s => {
    const b = document.createElement("button");
    b.className = "list-btn";
    b.innerHTML = `<b>${s.number}. ${safe(s.englishName)}</b>
     <div class="arabic">${safe(s.name)}</div>
     <span class="small">${s.numberOfAyahs} oyat</span>`;
    b.onclick = () => loadSurah(s.number,s.englishName);
    $("surahList").appendChild(b);
   });
  };
  $("surahSearch").oninput = draw;
  draw();
 } catch (e) {
  $("content").innerHTML = '<div class="note">Suralar yuklanmadi. Internetni tekshirib, qayta urinib ko‘ring.</div><button class="btn" id="retry">Qayta urinish</button>';
  $("retry").onclick = loadSuras;
 }
}

async function loadSurah(number,name) {
 page(name,"<p>Oyatlar yuklanmoqda...</p>");
 try {
  const [arabic,translation] = await Promise.all([
   getJSON(`https://api.alquran.cloud/v1/surah/${number}/quran-uthmani`),
   getJSON(`https://api.alquran.cloud/v1/surah/${number}/uz.sodik`)
  ]);
  const verses = arabic.data.ayahs;
  const translated = translation.data.ayahs;
  $("content").innerHTML = `
   <button class="btn" id="surahBack">← Suralar</button>
   <h3>${safe(name)}</h3>
   <label for="qari">Qiroatni tanlang</label>
   <select id="qari">${RECITERS.map((r,i)=>`<option value="${i}">${safe(r.name)}</option>`).join("")}</select>
   <audio id="surahAudio" controls preload="metadata"></audio>
   <button class="btn gold" id="playAudio">▶ Qiroatni tinglash</button>
   <div id="verseList"></div>`;
  $("surahBack").onclick = loadSuras;
  $("playAudio").onclick = () => {
   const reciter = RECITERS[Number($("qari").value)];
   $("surahAudio").src =
    `https://cdn.islamic.network/quran/audio-surah/128/${reciter.id}/${number}.mp3`;
   $("surahAudio").play().catch(() => alert("Bu qori audiosi manbada topilmadi yoki ijro etilmadi."));
  };
  $("verseList").innerHTML = verses.map((v,i) => `
   <article class="item">
    <div class="arabic">${safe(v.text)} ۞ ${v.numberInSurah}</div>
    <p>${safe(translated[i]?.text || "Tarjima mavjud emas")}</p>
   </article>`).join("");
 } catch (e) {
  $("content").innerHTML = '<div class="note">Sura matni yoki tarjimasi yuklanmadi. Qayta urinib ko‘ring.</div><button class="btn" id="retrySurah">Qayta urinish</button>';
  $("retrySurah").onclick = () => loadSurah(number,name);
 }
}

/* Qiroatlar */
async function recitation() {
 page("Qur’on qiroatlari",`
  <p>Qorini tanlang va 114 suradan birini bosing.</p>
  <select id="reciter">${RECITERS.map((r,i)=>`<option value="${i}">${safe(r.name)}</option>`).join("")}</select>
  <input id="recSearch" placeholder="Sura qidirish">
  <div id="recList"></div>`);
 try {
  if (!suras.length) {
   const data = await getJSON("https://api.alquran.cloud/v1/surah");
   suras = data.data || [];
  }
  const draw = () => {
   const q = $("recSearch").value.toLowerCase();
   $("recList").innerHTML = "";
   suras.filter(s => (s.englishName+" "+s.number).toLowerCase().includes(q)).forEach(s => {
    const b = document.createElement("button");
    b.className = "list-btn";
    b.textContent = `${s.number}. ${s.englishName} — ${s.name}`;
    b.onclick = () => {
     const r = RECITERS[Number($("reciter").value)];
     page("Qiroat — "+s.englishName,`
      <button class="btn" id="recBack">← Qorilar ro‘yxati</button>
      <p>${safe(r.name)}</p>
      <p class="arabic">${safe(s.name)}</p>
      <audio id="recAudio" controls preload="metadata" src="https://cdn.islamic.network/quran/audio-surah/128/${r.id}/${s.number}.mp3"></audio>
      <p class="small">Pleyerda vaqt, pauza va davom ettirish boshqaruvlari mavjud. Audio manbasi ishlashi internet va manba mavjudligiga bog‘liq.</p>`);
     $("recBack").onclick = recitation;
    };
    $("recList").appendChild(b);
   });
  };
  $("recSearch").oninput = draw;
  draw();
 } catch(e) {
  $("content").innerHTML = '<div class="note">Qiroat ro‘yxatini yuklab bo‘lmadi.</div>';
 }
}

/* Tasbeh */
function tasbih(index = 0) {
 zikrIndex = index % ZIKR.length;
 zikrCount = 0;
 const z = ZIKR[zikrIndex];
 page("Tasbeh",`
  <div class="arabic">${z.a}</div>
  <h3>${safe(z.t)}</h3>
  <p>${safe(z.m)}</p>
  <div class="note">Manba: ${safe(z.src)}. Takror soni aynan zikrning shakliga mos tekshirilishi lozim.</div>
  <div class="counter">
   <div class="count" id="counter">0 / ${z.n}</div>
   <button class="count-btn" id="countButton">ZIKR</button>
   <p><button class="btn" id="reset">Sanoqni tiklash</button>
   <button class="btn gold" id="next">Keyingi zikr →</button></p>
  </div>`);
 $("countButton").onclick = () => {
  if (zikrCount < z.n) zikrCount++;
  $("counter").textContent = `${zikrCount} / ${z.n}`;
  if (window.Telegram?.WebApp?.HapticFeedback) {
   window.Telegram.WebApp.HapticFeedback.impactOccurred("light");
  }
  if (zikrCount === z.n) alert("Sanoq tugadi. Keyingi zikrga o‘tishingiz mumkin.");
 };
 $("reset").onclick = () => {
  zikrCount = 0;
  $("counter").textContent = `0 / ${z.n}`;
 };
 $("next").onclick = () => tasbih(zikrIndex+1);
}

function adhkar(kind) {
 page(kind==="morning"?"Tonggi zikrlar":"Kechki zikrlar",
  '<p class="muted">Zikrni tanlang. Har bir zikrning to‘liq sahih manbasi va takror sonini alohida tekshirish zarur.</p><div id="adhkarList"></div>');
 ZIKR.forEach((z,i) => {
  const b = document.createElement("button");
  b.className = "list-btn";
  b.innerHTML = `<div class="arabic">${z.a}</div><b>${safe(z.t)}</b><br><span class="small">${safe(z.src)}</span>`;
  b.onclick = () => tasbih(i);
  $("adhkarList").appendChild(b);
 });
}

/* Namoz vaqtlari */
async function showPrayerTimes(city,target="prayers",status="prayerStatus") {
 if (!city.trim()) {
  if ($(status)) $(status).textContent = "Shahar nomini kiriting.";
  return;
 }
 if ($(status)) $(status).textContent = "Namoz vaqtlari olinmoqda...";
 try {
  const data = await getJSON(`https://api.aladhan.com/v1/timingsByCity?city=${encodeURIComponent(city)}&country=&method=3`);
  const t = data.data.timings;
  const vals = [["Bomdod",t.Fajr],["Peshin",t.Dhuhr],["Asr",t.Asr],["Shom",t.Maghrib],["Xufton",t.Isha]];
  $(target).innerHTML = vals.map(([n,v])=>`<div class="prayer"><b>${n}</b><span>${safe(v)}</span></div>`).join("");
  if ($(status)) $(status).textContent = `Shahar: ${city}. Vaqtlarni mahalliy masjid taqvimi bilan tekshiring.`;
 } catch(e) {
  if ($(status)) $(status).textContent = "Vaqtlar olinmadi. Shahar nomi yoki internetni tekshiring.";
 }
}
async function prayerPage() {
 page("Namoz vaqtlari",`
  <p>Shahar nomini kiriting. Boshqa davlatdagi shaharlar uchun ham qidirish mumkin.</p>
  <input id="citySearch" placeholder="Masalan, Karaganda, Almaty, Tashkent">
  <button class="btn gold" id="cityLoad">Namoz vaqtlarini olish</button>
  <div class="prayers" id="cityPrayers"></div>
  <p id="cityStatus" class="small"></p>`);
 $("cityLoad").onclick = () => showPrayerTimes($("citySearch").value,"cityPrayers","cityStatus");
}

/* Siyrat o‘yini — namuna savollar. Katta, manbalari tekshirilgan savollar bazasi hali alohida qo‘shilishi kerak. */
const QUESTIONS = [
 {q:"Payg‘ambarimiz ﷺ qaysi shaharda tug‘ilganlar?",a:["Makka","Madina","Toif","Quddus"],correct:0,why:"Payg‘ambarimiz ﷺ Makkada tavallud topganlar."},
 {q:"Birinchi vahiy qaysi g‘orda nozil bo‘lgan?",a:["Savr","Hiro","Uhud","Quba"],correct:1,why:"Birinchi vahiy Hiro g‘orida nozil bo‘lgan."},
 {q:"Hijrat qaysi shaharga bo‘lgan?",a:["Shom","Yaman","Madina","Toif"],correct:2,why:"Musulmonlar Madinaga hijrat qilganlar."}
];
function quiz() {
 quizScore = 0;
 quizIndex = 0;
 quizQuestions = [...QUESTIONS].sort(()=>Math.random()-0.5);
 showQuestion();
}
function showQuestion() {
 if (quizIndex >= quizQuestions.length) {
  page("O‘yin yakuni",`<h3>Natija: ${quizScore} / ${quizQuestions.length}</h3><p>Bu hozircha kichik namuna. To‘liq 50 savolli, umumiy reytingga ulangan o‘yin uchun tekshirilgan savollar bazasi va server ball mexanizmi kerak.</p><button class="btn gold" id="playAgain">Qayta o‘ynash</button>`);
  $("playAgain").onclick = quiz;
  return;
 }
 const q = quizQuestions[quizIndex];
 page(`Siyrat o‘yini — ${quizIndex+1}/${quizQuestions.length}`,
  `<h3>${safe(q.q)}</h3><div id="answers"></div><div id="explanation"></div>`);
 q.a.forEach((answer,i) => {
  const b = document.createElement("button");
  b.className = "list-btn";
  b.textContent = `${"ABCD"[i]}. ${answer}`;
  b.onclick = () => {
   document.querySelectorAll("#answers button").forEach(x=>x.disabled=true);
   const correct = i===q.correct;
   if (correct) quizScore++;
   $("explanation").innerHTML = `<div class="note">${correct?"To‘g‘ri javob!":"To‘g‘ri javob: "+safe(q.a[q.correct])}<br>${safe(q.why)}</div><button class="btn gold" id="nextQuestion">Keyingi savol</button>`;
   $("nextQuestion").onclick = () => {quizIndex++;showQuestion();};
  };
  $("answers").appendChild(b);
 });
}

/* Bo‘limlar */
function openPage(id) {
 if (id==="quran") return loadSuras();
 if (id==="recitation") return recitation();
 if (id==="tasbih") return tasbih();
 if (id==="morning"||id==="evening") return adhkar(id);
 if (id==="prayer") return prayerPage();
 if (id==="quiz") return quiz();

 if (id==="ai") {
  page("TAQVO AI",`
   <p>Islomiy savolingizni yozing.</p>
   <textarea id="question" rows="4" placeholder="Savolingiz..."></textarea>
   <button class="btn gold" id="ask">Savol yuborish</button>
   <div id="answer"></div>
   <p class="small">AI olim yoki mufti emas. Murakkab fatvolarni malakali olim bilan tekshiring.</p>`);
  $("ask").onclick = async () => {
   const question = $("question").value.trim();
   if (!question) return;
   $("answer").textContent = "Javob olinmoqda...";
   const init_data = window.Telegram?.WebApp?.initData || "";
   try {
    const response = await fetch(API+"/api/ask",{
     method:"POST",
     headers:{"Content-Type":"application/json"},
     body:JSON.stringify({question,init_data})
    });
    const result = await response.json();
    $("answer").textContent = response.ok ? result.answer : (result.detail || "AI xizmatida xato.");
   } catch(e) {
    $("answer").textContent = "Serverga ulanib bo‘lmadi. Render holatini tekshiring.";
   }
  };
  return;
 }

 if (id==="settings") {
  page("Til va havolalar",`
   <p>Til tanlang:</p>
   <button class="btn" id="latin">Lotin</button>
   <button class="btn gold" id="cyrillic">Кирилл</button>
   <p><a href="https://t.me/hakiymqalb" target="_blank" rel="noopener">Telegram kanali</a></p>
   <p>Instagram havolasini haqiqiy profilingiz bilan sozlash kerak.</p>`);
  $("latin").onclick = () => setLanguage(false);
  $("cyrillic").onclick = () => setLanguage(true);
  return;
 }

 const info = {
  duas:"Sahih duolar: arabcha matn, tarjima, fazilat va aniq Qur’on/hadis manbalari bilan to‘liq to‘plam alohida tekshirib kiritilishi kerak.",
  hadith:"100 sahih hadis: arabcha matn, o‘zbekcha tarjima va aniq manba raqamlari bilan to‘liq to‘plam hali qo‘shilishi kerak.",
  forty:"Qirq farz matni ishonchli manba va tanlangan ta’lim an’anasi bilan tekshirib kiritilishi kerak.",
  duties:"Asosiy burchlar bo‘limiga dalillar va mazhab farqlari tekshirilgan kontent qo‘shilishi kerak.",
  foundations:"Islom asoslari Qur’on, sahih hadis va ishonchli ilmiy sharhlar asosida to‘ldirilishi kerak.",
  sirah:"Siyrat voqealari bosqichma-bosqich, manbalari va rivoyat darajalari bilan to‘ldirilishi kerak.",
  ranking:"Haqiqiy global reyting uchun doimiy ma’lumotlar bazasi va server ball tekshiruvlari kerak.",
  media:"Faqat qonuniy va tekshirilgan video manbalari joylashtirilishi kerak."
 };
 const selected = MENU.find(x=>x[0]===id);
 page(selected?selected[2]:"TAQVO PRO MAX",`<div class="note">${safe(info[id]||"Bu bo‘lim uchun tekshirilgan kontent va tegishli xizmat integratsiyasi kerak.")}</div>`);
}

/* Lotin/kirill rejimi — menyu va asosiy sarlavhalar */
function setLanguage(toCyr) {
 isCyrillic = toCyr;
 $("language").textContent = isCyrillic ? "Lotin" : "Кирилл";
 $("allHeading").textContent = isCyrillic ? "17 та бўлим" : "17 ta bo‘lim";
 $("prayerHeading").textContent = isCyrillic ? "Намоз вақтлари" : "Namoz vaqtlari";
 $("heroTitle").textContent = isCyrillic ? "Қуръон ва зикр билан қалбни ёритинг" : "Qur’on va zikr bilan qalbni yoriting";
 $("heroDesc").textContent = isCyrillic ? "Ишончли манбалар ва фойдали ибодатлар бир жойда." : "Ishonchli manbalar va foydali ibodatlar bir joyda.";
 renderMenu($("search").value);
}

/* Ishga tushirish */
$("language").onclick = () => setLanguage(!isCyrillic);
$("search").addEventListener("input",e=>renderMenu(e.target.value));
$("loadPrayer").onclick = () => showPrayerTimes($("city").value,"prayers","prayerStatus");
document.querySelectorAll("[data-open]").forEach(button=>{
 button.addEventListener("click",()=>openPage(button.dataset.open));
});
if (window.Telegram?.WebApp) {
 window.Telegram.WebApp.ready();
 window.Telegram.WebApp.expand();
}
renderMenu();
