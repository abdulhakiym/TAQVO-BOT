
"use strict";

const API = "https://taqvo-bot-api.onrender.com";
const $ = id => document.getElementById(id);

const MENU = [
 ["quran","📖","Qur’oni Karim","114 sura va o‘qish"],
 ["recitation","🎧","Qur’on qiroatlari","Qorilar va audio"],
 ["tasbih","📿","Tasbeh","Zikr va sanoq"],
 ["morning","🌅","Tonggi zikrlar","Tonggi zikrlar to‘plami"],
 ["evening","🌙","Kechki zikrlar","Kechki zikrlar to‘plami"],
 ["prayer","🕌","Namoz vaqtlari","Shahar bo‘yicha"],
 ["duas","🤲","Sahih duolar","Duo va ma’nolari"],
 ["hadith","📜","Hadislar","Hadislar to‘plami"],
 ["forty","☪️","Qirq farz","O‘rganish va yodlash"],
 ["duties","🧭","Asosiy burchlar","Diniy bilimlar"],
 ["foundations","🌿","Islom asoslari","Islomni o‘rganish"],
 ["sirah","🕋","Payg‘ambarimiz ﷺ siyratlari","Siyrat bosqichlari"],
 ["quiz","🎯","Siyrat o‘yini","Savollar va ballar"],
 ["ranking","🏆","Reyting","Medallar va natijalar"],
 ["media","🎬","Islomiy kino va multfilmlar","Video manbalari"],
 ["ai","🤖","TAQVO AI","Islomiy savol-javob"],
 ["settings","🔤","Til va havolalar","Sozlamalar"]
];

const ZIKR = [
 {a:"سُبْحَانَ اللَّهِ",t:"Subhanalloh",m:"Alloh barcha nuqsonlardan pokdir.",n:33,src:"Sahih Muslim 597"},
 {a:"الْحَمْدُ لِلَّهِ",t:"Alhamdulillah",m:"Barcha hamd Allohgadir.",n:33,src:"Sahih Muslim 597"},
 {a:"اللَّهُ أَكْبَرُ",t:"Allohu akbar",m:"Alloh eng buyukdir.",n:34,src:"Sahih Muslim 597"},
 {a:"أَسْتَغْفِرُ اللَّهَ",t:"Astag‘firulloh",m:"Allohdan mag‘firat so‘rayman.",n:3,src:"Sahih Muslim 591"},
 {a:"لَا إِلَهَ إِلَّا اللَّهُ",t:"La ilaha illalloh",m:"Allohdan boshqa haq iloh yo‘q.",n:100,src:"Sahih Muslim 2691"}
];

let cyr = false, zikrIndex = 0, zikrCount = 0, suras = [], quizIndex = 0, quizScore = 0, quizSet = [];

function safe(s){return String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}

function renderMenu(filter=""){
 $("menu").innerHTML="";
 MENU.filter(x=>(x[2]+" "+x[3]).toLowerCase().includes(filter.toLowerCase())).forEach(x=>{
  const b=document.createElement("button"); b.className="tile";
  b.innerHTML=`<span class="emoji">${x[1]}</span><b>${safe(x[2])}</b><small>${safe(x[3])}</small>`;
  b.onclick=()=>openPage(x[0]); $("menu").appendChild(b);
 });
}

function page(title,html){
 $("pageTitle").textContent=title; $("content").innerHTML=html;
 $("page").classList.remove("hidden"); $("menu").classList.add("hidden");
 $("search").classList.add("hidden"); $("allHeading").classList.add("hidden");
 window.scrollTo({top:0,behavior:"smooth"});
}
function home(){
 $("page").classList.add("hidden"); $("menu").classList.remove("hidden");
 $("search").classList.remove("hidden"); $("allHeading").classList.remove("hidden");
 window.scrollTo({top:0,behavior:"smooth"});
}
$("back").onclick=home;

async function getJson(url){
 const r=await fetch(url); if(!r.ok)throw Error("Xizmat javob bermadi: "+r.status); return r.json();
}

async function loadSuras(){
 page("Qur’oni Karim",'<p class="muted">Suralar ishonchli Qur’on API manbasidan yuklanmoqda...</p>');
 try{
  const d=await getJson("https://api.alquran.cloud/v1/surah");
  suras=d.data||[];
  $("content").innerHTML=`<input id="surahSearch" placeholder="Sura nomini qidirish..."><div id="surahList"></div>`;
  const draw=()=>{
   const q=$("surahSearch").value.toLowerCase();
   $("surahList").innerHTML="";
   suras.filter(s=>(s.name+" "+s.englishName+" "+s.number).toLowerCase().includes(q)).forEach(s=>{
    const b=document.createElement("button"); b.className="list-btn";
    b.innerHTML=`<b>${s.number}. ${safe(s.englishName)}</b><br><span class="arabic">${safe(s.name)}</span><span class="small">${s.numberOfAyahs} oyat</span>`;
    b.onclick=()=>loadSurah(s.number,s.englishName); $("surahList").appendChild(b);
   });
  };
  $("surahSearch").oninput=draw; draw();
 }catch(e){$("content").innerHTML=`<div class="note">Qur’on API hozir ulanmagan. Internet aloqasini tekshirib, qayta urinib ko‘ring.</div>`;}
}
async function loadSurah(n,name){
 page(name,"<p>Oyatlar yuklanmoqda...</p>");
 try{
  const d=await getJson(`https://api.alquran.cloud/v1/surah/${n}/quran-uthmani`);
  const tr=await getJson(`https://api.alquran.cloud/v1/surah/${n}/uz.sodik`);
  const verses=d.data.ayahs, trans=tr.data.ayahs;
  $("content").innerHTML=`<div class="row"><button class="btn" id="surahBack">← Suralar</button><button class="btn" id="playSurah">▶ Qiroat</button></div><audio id="qAudio" controls preload="none"></audio><div id="verses"></div>`;
  $("surahBack").onclick=loadSuras;
  $("playSurah").onclick=()=>{ $("qAudio").src=`https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/${n}.mp3`; $("qAudio").play().catch(()=>alert("Audio ochilmadi. Internet yoki audio manbasini tekshiring.")); };
  $("verses").innerHTML=verses.map((v,i)=>`<article class="item"><div class="arabic">${safe(v.text)} ۞ ${v.numberInSurah}</div><p>${safe(trans[i]?.text||"Tarjima mavjud emas")}</p></article>`).join("");
 }catch(e){$("content").innerHTML=`<div class="note">Sura matni yuklanmadi. Internetni tekshirib, qayta urinib ko‘ring.</div><button class="btn" id="retrySurah">Qayta urinish</button>`;$("retrySurah").onclick=()=>loadSurah(n,name);}
}

const RECITERS=[
 ["Mishary Rashid Alafasy","ar.alafasy"],
 ["Abdul Basit","ar.abdulbasitmurattal"],
 ["Maher Al Muaiqly","ar.mahermuaiqly"],
 ["Abdurrahman As-Sudais","ar.abdurrahmaansudais"],
 ["Saud Al-Shuraim","ar.saoodshuraym"],
 ["Hani Ar-Rifai","ar.hanirifai"]
];
async function recitation(){
 page("Qur’on qiroatlari",'<p>Qorini va surani tanlang.</p><select id="reciter"></select><div id="recSuras"></div>');
 $("reciter").innerHTML=RECITERS.map((r,i)=>`<option value="${i}">${safe(r[0])}</option>`).join("");
 try{
  if(!suras.length){const d=await getJson("https://api.alquran.cloud/v1/surah");suras=d.data;}
  $("recSuras").innerHTML=`<input id="recSearch" placeholder="Sura qidirish"><div id="recList"></div>`;
  const draw=()=>{
   const q=$("recSearch").value.toLowerCase(); $("recList").innerHTML="";
   suras.filter(s=>(s.englishName+" "+s.number).toLowerCase().includes(q)).forEach(s=>{
    const b=document.createElement("button");b.className="list-btn";
    b.textContent=s.number+". "+s.englishName+" — "+s.name;
    b.onclick=()=>{
     const r=RECITERS[Number($("reciter").value)];
     page("Qiroat: "+s.englishName,`<p class="arabic">${safe(s.name)}</p><p>${safe(r[0])}</p><audio controls autoplay src="https://cdn.islamic.network/quran/audio-surah/128/${r[1]}/${s.number}.mp3"></audio><p class="small">Agar audio ishlamasa, ushbu qori uchun audio identifikatori manbada mavjud emas bo‘lishi mumkin.</p>`);
    };$("recList").appendChild(b);
   });
  };
  $("recSearch").oninput=draw;draw();
 }catch(e){$("content").innerHTML='<div class="note">Qiroat ro‘yxatini yuklab bo‘lmadi. Internetni tekshiring.</div>';}
}

function tasbih(idx=0){
 zikrIndex=idx%ZIKR.length; zikrCount=0; const z=ZIKR[zikrIndex];
 page("Tasbeh",`<div class="arabic">${z.a}</div><h3>${safe(z.t)}</h3><p>${safe(z.m)}</p><div class="note">Manba: ${safe(z.src)}. Takror sonini diniy manba va zikrning aynan shu shakliga qarab tekshiring.</div><div class="counter"><div class="count" id="counter">0 / ${z.n}</div><button class="count-btn" id="countButton">ZIKR</button><p><button class="btn" id="reset">Sanoqni tiklash</button> <button class="btn gold" id="next">Keyingi zikr →</button></p></div>`);
 $("countButton").onclick=()=>{
  if(zikrCount<z.n)zikrCount++;
  $("counter").textContent=zikrCount+" / "+z.n;
  if(window.Telegram?.WebApp?.HapticFeedback)window.Telegram.WebApp.HapticFeedback.impactOccurred("light");
  if(zikrCount===z.n)alert("Sanoq tugadi. Keyingi zikrga o‘tishingiz mumkin.");
 };
 $("reset").onclick=()=>{zikrCount=0;$("counter").textContent="0 / "+z.n;};
 $("next").onclick=()=>tasbih(zikrIndex+1);
}

function adhkar(kind){
 page(kind==="morning"?"Tonggi zikrlar":"Kechki zikrlar",`<p class="muted">Quyidagi zikrlar ro‘yxati umumiy tasbeh namunalari bilan cheklangan. To‘liq 14–15 ta ertalabki yoki kechki zikrlar manbasi va takror sonlari tekshirilgan holda alohida jamlanishi kerak.</p><div id="adhkarList"></div>`);
 ZIKR.forEach((z,i)=>{
  const b=document.createElement("button");b.className="list-btn";b.innerHTML=`<span class="arabic">${z.a}</span><b>${safe(z.t)}</b><br><span class="small">${safe(z.src)}</span>`;
  b.onclick=()=>tasbih(i);$("adhkarList").appendChild(b);
 });
}

async function prayerTimes(){
 const city=$("city").value.trim(); if(!city){$("prayerStatus").textContent="Shahar nomini kiriting.";return;}
 $("prayerStatus").textContent="Namoz vaqtlari olinmoqda...";
 try{
  const d=await getJson(`https://api.aladhan.com/v1/timingsByCity?city=${encodeURIComponent(city)}&country=&method=3`);
  const t=d.data.timings;
  const vals=[["Bomdod",t.Fajr],["Peshin",t.Dhuhr],["Asr",t.Asr],["Shom",t.Maghrib],["Xufton",t.Isha]];
  $("prayers").innerHTML=vals.map(([n,v])=>`<div class="prayer"><b>${n}</b><span>${safe(v)}</span></div>`).join("");
  $("prayerStatus").textContent="Manba: AlAdhan. Hisoblash usuli va mahalliy vaqtni shahringiz bo‘yicha tekshiring.";
 }catch(e){$("prayerStatus").textContent="Namoz vaqtlari olinmadi. Shahar nomi va internetni tekshiring.";}
}

function generic(title,text){page(title,`<div class="note">${safe(text)}</div>`);}
function openPage(id){
 if(id==="quran")return loadSuras();
 if(id==="recitation")return recitation();
 if(id==="tasbih")return tasbih();
 if(id==="morning"||id==="evening")return adhkar(id);
 if(id==="prayer"){page("Namoz vaqtlari",'<p>Shaharni kiriting va yangilang.</p><div class="row"><input id="city2" placeholder="Masalan, Tashkent"><button class="btn gold" id="p2">Yangilash</button></div><div id="presult"></div>');$("p2").onclick=async()=>{const city=$("city2").value.trim();try{const d=await getJson(`https://api.aladhan.com/v1/timingsByCity?city=${encodeURIComponent(city)}&country=&method=3`);$("presult").innerHTML=Object.entries({Bomdod:d.data.timings.Fajr,Peshin:d.data.timings.Dhuhr,Asr:d.data.timings.Asr,Shom:d.data.timings.Maghrib,Xufton:d.data.timings.Isha}).map(([k,v])=>`<div class="item">${k}: <b>${safe(v)}</b></div>`).join("");}catch(e){$("presult").textContent="Vaqtlar olinmadi.";}};return;}
 if(id==="settings")return page("Til va havolalar",'<p>Saytning ayrim matnlari tarjima qilinadi. Bu sozlama hali barcha kontentni to‘liq tarjima qilmaydi.</p><button class="btn" id="latin">Lotin</button> <button class="btn gold" id="cyrillic">Кирилл</button><p><a href="https://t.me/hakiymqalb">Telegram kanali</a></p><p>Instagram havolasi keyin sozlanadi.</p>') || (()=>{$("latin").onclick=()=>setLanguage(false);$("cyrillic").onclick=()=>setLanguage(true);})();
 const info={
  duas:"Duolar bo‘limiga arabcha matn, tarjima va ishonchli hadis/Qur’on manbalarini tekshirib kiritish kerak.",
  hadith:"100 hadis to‘plami uchun har bir hadisning arabcha matni, tarjimasi va aniq nashr/raqam ma’lumotlari tekshirilishi kerak.",
  forty:"Qirq farz matni tanlangan ta’lim an’anasi va manbalar bilan tekshirib joylashtirilishi kerak.",
  duties:"Asosiy burchlar: ishonchli dalillar va mazhab farqlari bilan tuzilgan kontent kerak.",
  foundations:"Islom asoslari: Qur’on, sahih hadis va ishonchli ilmiy izohlar asosida tuziladi.",
  sirah:"Siyrat voqealari bosqichma-bosqich va rivoyatlarning ishonchlilik darajasi bilan berilishi kerak.",
  quiz:"50 savolli tasodifiy o‘yin va global ballar uchun serverdagi savollar bazasi, foydalanuvchi identifikatsiyasi va anti-abuse mexanizmi kerak.",
  ranking:"Haqiqiy global reyting uchun server ma’lumotlar bazasi zarur. Hozircha bu sahifada real reyting ko‘rsatilmaydi.",
  media:"Faqat qonuniy tomosha manbalarini joylashtirish mumkin. Tasdiqlanmagan video havolalari qo‘shilmaydi.",
  ai:"TAQVO AI uchun AI provayderi kaliti va ishonchli diniy manbalar bilan tekshiriladigan server integratsiyasi kerak."
 };
 if(id==="ai"){
  return page("TAQVO AI",'<p>Islomiy savolingizni yozing.</p><textarea id="question" rows="4" placeholder="Savolingiz..."></textarea><button class="btn gold" id="ask">Savol yuborish</button><div id="answer"></div><p class="small">AI olim yoki shayx emas. Javoblarni malakali olim bilan tekshirish zarur.</p>') || (()=>{$("ask").onclick=async()=>{const q=$("question").value.trim();if(!q)return;try{const r=await fetch(API+"/api/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question:q})});const d=await r.json();$("answer").textContent=d.answer||d.detail||"Javob mavjud emas";}catch(e){$("answer").textContent="AI serveri ulanmagan yoki xato berdi.";}}})();
 }
 generic(MENU.find(x=>x[0]===id)?.[2]||"TAQVO",info[id]||"Bu bo‘lim uchun ishonchli kontent va tegishli xizmat integratsiyasi talab qilinadi.");
}

function setLanguage(toCyr){
 cyr=toCyr;
 $("language").textContent=cyr?"Lotin":"Кирилл";
 $("allHeading").textContent=cyr?"17 та бўлим":"17 ta bo‘lim";
 $("prayerHeading").textContent=cyr?"Намоз вақтлари":"Namoz vaqtlari";
 $("heroTitle").textContent=cyr?"Қуръон ва зикр билан қалбни ёритинг":"Qur’on va zikr bilan qalbni yoritинг";
 $("heroDesc").textContent=cyr?"Ишончли манбалар ва фойдали ибодатлар бир жойда.":"Ishonchli manbalar va foydali ibodatlar bir joyda.";
 renderMenu($("search").value);
}
$("language").onclick=()=>setLanguage(!cyr);
$("search").addEventListener("input",e=>renderMenu(e.target.value));
$("loadPrayer").onclick=prayerTimes;
document.querySelectorAll("[data-open]").forEach(b=>b.addEventListener("click",()=>openPage(b.dataset.open)));
if(window.Telegram?.WebApp){window.Telegram.WebApp.ready();window.Telegram.WebApp.expand();}
renderMenu();
