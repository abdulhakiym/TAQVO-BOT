
"use strict";

const SERVER = "https://taqvo-bot-api.onrender.com";

const sections = [
  ["1","📖","Qur’oni Karim","114 sura, sahifama-sahifa o‘qish"],
  ["2","🎧","Qur’on qiroatlari","6 qori va 114 sura audiosi"],
  ["3","📿","Tasbeh","Zikrlar, fazilatlar va sanoq"],
  ["4","🌅","Tonggi va kechki zikrlar","14–15 tadan zikrli papkalar"],
  ["5","🕌","Namoz vaqtlari","Shahar bo‘yicha namoz va eslatmalar"],
  ["6","🤲","Sahih duolar","Arabcha matn va o‘zbekcha ma’no"],
  ["7","📜","Hadislar","Buxoriy va Muslimdan 100 hadis"],
  ["8","☪️","Qirq farz","Yodlash uchun qulay qo‘llanma"],
  ["9","🧭","Asosiy burchlar","Dalillar bilan tushuntirish"],
  ["10","🌿","Islom asoslari","Asosiy tushunchalar va dalillar"],
  ["11","🕋","Payg‘ambarimiz ﷺ siyratlari","Bosqichma-bosqich siyrat"],
  ["12","🎯","Siyrat o‘yini","50 savol va ballar"],
  ["13","🏆","Reyting","Medallar va global reyting"],
  ["14","🎬","Islomiy kino va multfilmlar","O‘zbek tilidagi materiallar"],
  ["15","🤖","TAQVO AI","Dalilli islomiy savol-javob"],
  ["16","🔤","Til sozlamalari","Lotin va кирилл yozuvi"],
  ["17","🔗","Ijtimoiy tarmoqlar","Telegram va Instagram"]
];

const translations = {
  "Qur’oni Karim":"Қуръони Карим",
  "Qur’on qiroatlari":"Қуръон қироатлари",
  "Tasbeh":"Тасбеҳ",
  "Tonggi va kechki zikrlar":"Тонгги ва кечки зикрлар",
  "Namoz vaqtlari":"Намоз вақтлари",
  "Sahih duolar":"Саҳиҳ дуолар",
  "Hadislar":"Ҳадислар",
  "Qirq farz":"Қирқ фарз",
  "Asosiy burchlar":"Асосий бурчлар",
  "Islom asoslari":"Ислом асослари",
  "Payg‘ambarimiz ﷺ siyratlari":"Пайғамбаримиз ﷺ сийратлари",
  "Siyrat o‘yini":"Сийрат ўйини",
  "Reyting":"Рейтинг",
  "Islomiy kino va multfilmlar":"Исломий кино ва мультфильмлар",
  "Til sozlamalari":"Тил созламалари",
  "Ijtimoiy tarmoqlar":"Ижтимоий тармоқлар"
};

const $ = id => document.getElementById(id);
let cyrillic = false;
let currentSection = null;
let dhikrCount = 0;

function showMessage(title, text) {
  $("detailNumber").textContent = "TAQVO PRO MAX";
  $("detailTitle").textContent = title;
  $("detailContent").innerHTML =
    `<div class="note">${escapeHtml(text)}</div>
     <p class="muted">Bu bo‘limning to‘liq ishlashi uchun tekshirilgan kontent yoki server API ulanishi kerak. Ulanmagan xizmat ishlayapti deb ko‘rsatilmaydi.</p>`;
  $("sections").classList.add("hidden");
  $("search").classList.add("hidden");
  $("detail").classList.remove("hidden");
  window.scrollTo({top:0,behavior:"smooth"});
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"
  })[char]);
}

function renderSections(filter = "") {
  const list = $("sections");
  list.innerHTML = "";
  sections
    .filter(item => {
      const name = cyrillic ? (translations[item[2]] || item[2]) : item[2];
      return (name + " " + item[3]).toLowerCase().includes(filter.toLowerCase());
    })
    .forEach(item => {
      const name = cyrillic ? (translations[item[2]] || item[2]) : item[2];
      const button = document.createElement("button");
      button.className = "tile";
      button.innerHTML =
        `<span class="emoji">${item[1]}</span>
         <b>${escapeHtml(item[0] + ". " + name)}</b>
         <small>${escapeHtml(item[3])}</small>`;
      button.addEventListener("click", () => openSection(item[0]));
      list.appendChild(button);
    });
}

function openSection(id) {
  currentSection = id;
  const item = sections.find(section => section[0] === id);
  if (!item) return;

  $("sections").classList.add("hidden");
  $("search").classList.add("hidden");
  $("detail").classList.remove("hidden");
  $("detailNumber").textContent = "BO‘LIM " + id;
  $("detailTitle").textContent = item[2];

  if (id === "3") {
    renderTasbeh();
  } else if (id === "4") {
    $("detailContent").innerHTML = `
      <div class="item"><button class="outline-btn" id="morning">🌅 Tonggi zikrlar</button></div>
      <div class="item"><button class="outline-btn" id="evening">🌙 Kechki zikrlar</button></div>
      <p class="muted">Zikrlar to‘plami manbalari tekshirilgach to‘liq joylashtiriladi.</p>`;
    $("morning").onclick = () => showMessage("Tonggi zikrlar","Har bir zikr arabcha matni, tarjimasi, fazilati, manbasi va ishonchli sanadagi takror soni bilan taqdim etiladi.");
    $("evening").onclick = () => showMessage("Kechki zikrlar","Har bir zikr arabcha matni, tarjimasi, fazilati, manbasi va ishonchli sanadagi takror soni bilan taqdim etiladi.");
  } else if (id === "16") {
    $("detailContent").innerHTML = `
      <p>Sayt matnini lotin yoki kirill yozuvida ko‘rishni tanlang.</p>
      <button class="gold-btn" id="latin">Lotin</button>
      <button class="outline-btn" id="cyr">Кирилл</button>`;
    $("latin").onclick = () => setLanguage(false);
    $("cyr").onclick = () => setLanguage(true);
  } else if (id === "17") {
    $("detailContent").innerHTML = `
      <p><a href="https://t.me/hakiymqalb" target="_blank" rel="noopener">Telegram: @hakiymqalb</a></p>
      <p>Instagram profilingizning aniq havolasi sozlamaga qo‘shilishi kerak.</p>`;
  } else if (id === "5") {
    $("detailContent").innerHTML = `
      <p>Tanlangan shahar: <b>${escapeHtml($("city").selectedOptions[0].textContent)}</b></p>
      <p class="muted">Aniq namoz vaqtlari serverga namoz vaqtlari manbasi ulangandan so‘ng ko‘rsatiladi.</p>
      <button class="outline-btn" id="reloadPrayer">Vaqtlarni yangilash</button>`;
    $("reloadPrayer").onclick = loadPrayerTimes;
  } else if (id === "12") {
    $("detailContent").innerHTML = `
      <p>Har bir o‘yin 50 ta tasodifiy siyrat savolidan iborat bo‘lishi rejalashtirilgan.</p>
      <p>Har bir to‘g‘ri javob: +20 ball. Yakuniy bonus miqdori belgilanmagan.</p>
      <p class="muted">Savollar bazasi va ballarni serverda saqlash ulanmaguncha haqiqiy reyting hisoblanmaydi.</p>`;
  } else if (id === "13") {
    $("detailContent").innerHTML = `
      <div class="item"><span class="medal">🥇</span> 1-o‘rin — Oltin</div>
      <div class="item"><span class="medal">🥈</span> 2-o‘rin — Kumush</div>
      <div class="item"><span class="medal">🥉</span> 3-o‘rin — Bronza</div>
      <p class="muted">Umumiy reyting server va ma’lumotlar bazasi ulangandan keyin ishlaydi.</p>`;
  } else {
    showMessage(item[2], item[3] + ". To‘liq matn, audio yoki xizmat tegishli ishonchli manbaga ulangach ishga tushiriladi.");
  }
}

function renderTasbeh() {
  dhikrCount = 0;
  $("detailContent").innerHTML = `
    <div class="arabic">سُبْحَانَ اللَّهِ</div>
    <p>Subhanalloh</p>
    <p class="muted">Ma’nosi: Alloh barcha nuqsonlardan pokdir.</p>
    <p class="muted">Bu boshlang‘ich namuna. To‘liq zikrlar va takror sonlari hadis manbalari tekshirilgach qo‘shiladi.</p>
    <div class="counter">
      <div class="count" id="count">0</div>
      <button class="count-btn" id="countBtn">ZIKR</button>
      <p><button class="outline-btn" id="resetCount">Sanoqni tiklash</button></p>
    </div>`;
  $("countBtn").onclick = () => {
    dhikrCount++;
    $("count").textContent = dhikrCount;
    if (window.Telegram?.WebApp?.HapticFeedback) {
      window.Telegram.WebApp.HapticFeedback.impactOccurred("light");
    }
  };
  $("resetCount").onclick = () => {
    dhikrCount = 0;
    $("count").textContent = "0";
  };
}

function setLanguage(toCyrillic) {
  cyrillic = toCyrillic;
  $("languageBtn").textContent = cyrillic ? "КИРИЛЛ / LOTIN" : "LOTIN / КИРИЛЛ";
  $("allTitle").textContent = cyrillic ? "Барча бўлимлар" : "Barcha bo‘limlar";
  $("quickTitle").textContent = cyrillic ? "Тезкор кириш" : "Tezkor kirish";
  $("prayerTitle").textContent = cyrillic ? "Намоз вақтлари" : "Namoz vaqtlari";
  $("heroTitle").textContent = cyrillic
    ? "Аллоҳни зикр қилиш билан қалблар ором топади."
    : "Allohni zikr qilish bilan qalblar orom topadi.";
  $("heroDesc").textContent = cyrillic
    ? "Қуръон, саҳиҳ зикрлар ва исломий билимлар — бир жойда."
    : "Qur’on, sahih zikrlar va islomiy bilimlar — bir joyda.";
  renderSections($("search").value);
}

async function loadPrayerTimes() {
  $("prayerStatus").textContent = "Namoz vaqtlari API orqali olinishi kerak.";
  try {
    const response = await fetch(`${SERVER}/api/prayer-times?city=${encodeURIComponent($("city").value)}`);
    if (!response.ok) throw new Error("API mavjud emas");
    const data = await response.json();
    const names = ["Bomdod","Peshin","Asr","Shom","Xufton"];
    $("prayers").innerHTML = names.map((name,index) => {
      const value = data.times?.[name] || data.times?.[index] || "--:--";
      return `<div class="prayer"><b>${name}</b><span>${escapeHtml(value)}</span></div>`;
    }).join("");
    $("prayerStatus").textContent = "Shahar: " + $("city").selectedOptions[0].textContent;
  } catch (error) {
    $("prayerStatus").textContent = "Namoz API ulanmagan. Hozircha aniq vaqtlar ko‘rsatilmayapti.";
  }
}

$("search").addEventListener("input", event => renderSections(event.target.value));
$("languageBtn").addEventListener("click", () => setLanguage(!cyrillic));
$("cityBtn").addEventListener("click", loadPrayerTimes);
$("back").addEventListener("click", () => {
  $("detail").classList.add("hidden");
  $("sections").classList.remove("hidden");
  $("search").classList.remove("hidden");
});
document.querySelectorAll("[data-open]").forEach(button => {
  button.addEventListener("click", () => openSection(button.dataset.open));
});

if (window.Telegram?.WebApp) {
  window.Telegram.WebApp.ready();
  window.Telegram.WebApp.expand();
}
renderSections();
