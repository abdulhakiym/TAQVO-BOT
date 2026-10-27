
"use strict";

(() => {
  const API = "https://taqvo-bot-api.onrender.com";
  const tg = window.Telegram?.WebApp;

  tg?.ready();
  tg?.expand();

  const $ = (id) => document.getElementById(id);

  const sections = [
    ["quran", "📖", "Qur’oni Karim"],
    ["audio", "🎧", "Qur’on qiroatlari"],
    ["tasbeh", "📿", "Tasbeh"],
    ["morning", "🌅", "Tonggi zikrlar"],
    ["evening", "🌙", "Kechgi zikrlar"],
    ["prayer", "🕌", "Namoz vaqtlari"],
    ["duas", "🤲", "Sahih duolar"],
    ["hadith", "📜", "Hadislar"],
    ["farz", "✅", "Qirq farz"],
    ["duties", "🧭", "Asosiy burchlar"],
    ["basics", "☪️", "Islom asoslari"],
    ["sirah", "🌟", "Payg‘ambarimiz ﷺ siyrati"],
    ["quiz", "🎯", "Siyrat viktorinasi"],
    ["ranking", "🏆", "Umumiy reyting"],
    ["movies", "🎬", "Islomiy filmlar"],
    ["ai", "✨", "TAQVO AI"],
    ["settings", "⚙️", "Til va sozlamalar"]
  ];

  const state = {
    currentSection: null,
    surahs: [],
    zikrCounts: {},
    quizQuestions: [],
    quizIndex: 0,
    quizScore: 0,
    city: "Karagandy",
    country: "Kazakhstan",
    method: 3,
    language: "uz"
  };

  const adhkar = [
    {
      arabic: "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ",
      title: "Subhanallohi va bihamdih",
      meaning: "Allohni hamd bilan poklab yod etaman.",
      count: 100,
      source: "Sahih al-Buxoriy 6405; Sahih Muslim 2691."
    },
    {
      arabic: "أَسْتَغْفِرُ اللَّهَ",
      title: "Astag‘firulloh",
      meaning: "Allohdan mag‘firat so‘rayman.",
      count: 3,
      source: "Sahih Muslim 591 — namozdan keyingi istig‘for."
    },
    {
      arabic: "سُبْحَانَ اللَّهِ",
      title: "Subhanalloh",
      meaning: "Alloh barcha nuqsonlardan pokdir.",
      count: 33,
      source: "Sahih Muslim 595 — namozdan keyingi tasbeh."
    },
    {
      arabic: "الْحَمْدُ لِلَّهِ",
      title: "Alhamdulillah",
      meaning: "Barcha hamd Allohga xosdir.",
      count: 33,
      source: "Sahih Muslim 595 — namozdan keyingi tasbeh."
    },
    {
      arabic: "اللَّهُ أَكْبَرُ",
      title: "Allohu akbar",
      meaning: "Alloh eng buyukdir.",
      count: 34,
      source: "Sahih Muslim 595 — namozdan keyingi zikr."
    }
  ];

  const quizBank = [
    {
      q: "Hijrat qaysi shaharga bo‘lgan?",
      a: ["Madina", "Shom", "Toif", "Yaman"],
      correct: 0,
      explanation: "Musulmonlar Makkadan Madinaga hijrat qilganlar."
    },
    {
      q: "Birinchi vahiy qaysi g‘orda nozil bo‘lgan?",
      a: ["Savr", "Hiro", "Uhud", "Qubo"],
      correct: 1,
      explanation: "Birinchi vahiy Hiro g‘orida nozil bo‘lgan."
    },
    {
      q: "Qur’onning birinchi surasi qaysi?",
      a: ["Baqara", "Ixlos", "Fotiha", "Nos"],
      correct: 2,
      explanation: "Mushaf tartibidagi birinchi sura Fotiha surasidir."
    },
    {
      q: "Badr jangi qaysi hijriy yilda bo‘lgan?",
      a: ["1-yil", "2-yil", "5-yil", "8-yil"],
      correct: 1,
      explanation: "Badr jangi hijratning ikkinchi yilida bo‘lgan."
    },
    {
      q: "Payg‘ambarimiz ﷺ qaysi qabiladan edilar?",
      a: ["Quraysh", "Aws", "Xazraj", "Saqqif"],
      correct: 0,
      explanation: "Rasululloh ﷺ Quraysh qabilasidan edilar."
    }
  ];

  function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    })[char]);
  }

  function apiHeaders() {
    return { "Content-Type": "application/json" };
  }

  async function apiFetch(path, options = {}) {
    const response = await fetch(API + path, options);
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(data.detail || "Server bilan bog‘lanishda xato.");
    }

    return data;
  }

  function renderMenu() {
    $("sectionMenu").innerHTML = sections.map(([id, icon, title]) => `
      <button class="tile" type="button" data-open="${id}">
        <span class="tile-icon">${icon}</span>
        <span class="tile-title">${title}</span>
        <span class="tile-sub">Bo‘limni ochish</span>
      </button>
    `).join("");
  }

  function showHome() {
    state.currentSection = null;
    $("homeScreen").classList.remove("hidden");
    $("sectionScreen").classList.add("hidden");
  }

  function showSection(id) {
    const section = sections.find((item) => item[0] === id);
    if (!section) return;

    state.currentSection = id;
    $("homeScreen").classList.add("hidden");
    $("sectionScreen").classList.remove("hidden");

    $("sectionContent").innerHTML = `
      <div class="card">
        <div class="muted">TAQVO PRO MAX</div>
        <h1>${section[1]} ${escapeHTML(section[2])}</h1>
      </div>
      ${sectionTemplate(id)}
    `;

    if (id === "quran") loadSurahs();
    if (id === "audio") renderAudioSection();
    if (["tasbeh", "morning", "evening"].includes(id)) renderAdhkar(id);
    if (id === "prayer") renderPrayerForm();
    if (id === "quiz") startQuiz();
    if (id === "ranking") loadRanking();
  }

  function sectionTemplate(id) {
    switch (id) {
      case "quran":
        return `
          <div class="card">
            <p class="muted">Qur’on suralarini yuklash uchun internet kerak.</p>
            <input class="field" id="surahSearch" placeholder="Sura qidirish...">
            <div id="surahList">Suralar yuklanmoqda...</div>
            <div id="ayahList"></div>
          </div>`;

      case "audio":
        return `
          <div class="card">
            <label for="reciterSelect">Qori tanlang</label>
            <select class="field" id="reciterSelect">
              <option value="ar.alafasy">Mishary Rashid Alafasy</option>
              <option value="ar.abdulbasitmurattal">Abdul Basit Abdus Samad</option>
              <option value="ar.abdurrahmaansudais">Abdurrahman As-Sudais</option>
              <option value="ar.husary">Mahmoud Khalil Al-Husary</option>
            </select>
            <p class="muted">Audio manbasi API tomonidan beriladi. Barcha qori identifikatorlari ushbu API’da mavjud bo‘lishi kafolatlanmaydi.</p>
            <div id="audioSurahList">Suralar yuklanmoqda...</div>
            <div id="audioPlayer"></div>
          </div>`;

      case "tasbeh":
      case "morning":
      case "evening":
        return `<div id="adhkarList"></div>`;

      case "prayer":
        return `
          <div class="card">
            <p class="muted">Namoz vaqtlari tashqi hisoblash API’sidan olinadi. Mahalliy masjid jadvalini ham tekshiring.</p>
            <div id="prayerForm"></div>
            <div id="prayerResult"></div>
          </div>`;

      case "duas":
        return `
          <div class="card">
            <h2>Qur’ondagi duo</h2>
            <div class="arabic">رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ</div>
            <p><b>Robbana atina fid-dunya hasanatan va fil-akhirati hasanatan va qina azaban-nar.</b></p>
            <p>Dunyoda ham, oxiratda ham yaxshilik ber va do‘zax azobidan saqla.</p>
            <p class="muted">Qur’on, Baqara 2:201.</p>
          </div>`;

      case "hadith":
        return `
          <div class="card">
            <h2>Niyat haqida</h2>
            <p>“Amallar niyatlarga bog‘liqdir.”</p>
            <p class="muted">Sahih al-Buxoriy 1; Sahih Muslim 1907.</p>
            <p class="muted">Bu hozircha namuna; 100 hadislik to‘liq kutubxona hali qo‘shilmagan.</p>
          </div>`;

      case "farz":
      case "duties":
      case "basics":
        return `
          <div class="card">
            <h2>O‘rganish bo‘limi</h2>
            <p>Bu bo‘limga ishonchli manbalar bilan tekshirilgan to‘liq darslar kiritilishi kerak.</p>
          </div>`;

      case "sirah":
        return `
          <div class="card">
            <h2>Rasululloh ﷺ siyrati</h2>
            <p>Siyrat voqealari manbalar va rivoyatlarning ishonchlilik darajasi bilan bosqichma-bosqich to‘ldirilishi kerak.</p>
          </div>`;

      case "quiz":
        return `<div id="quizContainer"></div>`;

      case "ranking":
        return `<div class="card"><div id="rankingContainer">Reyting yuklanmoqda...</div></div>`;

      case "movies":
        return `
          <div class="card">
            <h2>Video manbalari</h2>
            <p>Faqat qonuniy manbalardagi filmlar va multfilmlar havolalarini qo‘shing.</p>
            <a href="https://www.youtube.com/" target="_blank" rel="noopener">YouTube’ni ochish</a>
          </div>`;

      case "ai":
        return `
          <div class="card">
            <h2>TAQVO AI</h2>
            <textarea class="field" id="aiQuestion" rows="4" maxlength="4000" placeholder="Islomiy savolingizni yozing..."></textarea>
            <button class="gold-button" id="askAIButton" type="button">Javob olish</button>
            <div id="aiAnswer" class="list-item" aria-live="polite"></div>
            <p class="muted">AI xato qilishi mumkin. Muhim diniy masalada malakali olimga murojaat qiling.</p>
          </div>`;

      case "settings":
        return `
          <div class="card">
            <h2>Til va sozlamalar</h2>
            <p>Til tugmasi hozircha faqat tanlovni o‘zgartiradi. To‘liq lotin-kirill tarjimasi hali kiritilmagan.</p>
          </div>`;

      default:
        return `<div class="card">Bo‘lim topilmadi.</div>`;
    }
  }

  async function loadSurahs() {
    const list = $("surahList");

    try {
      const response = await fetch("https://api.alquran.cloud/v1/surah");
      if (!response.ok) throw new Error();

      const data = await response.json();
      state.surahs = data.data || [];
      renderSurahList();

      $("surahSearch").addEventListener("input", renderSurahList);
    } catch {
      list.textContent = "Suralar yuklanmadi. Internetni tekshiring.";
    }
  }

  function renderSurahList() {
    const query = ($("surahSearch")?.value || "").toLowerCase();

    $("surahList").innerHTML = state.surahs
      .filter((surah) =>
        `${surah.number} ${surah.englishName} ${surah.name}`
          .toLowerCase().includes(query)
      )
      .map((surah) => `
        <div class="list-item row">
          <div>
            <b>${surah.number}. ${escapeHTML(surah.englishName)}</b>
            <div class="muted">${escapeHTML(surah.name)} · ${surah.numberOfAyahs} oyat</div>
          </div>
          <button type="button" data-surah="${surah.number}">O‘qish</button>
        </div>
      `).join("");
  }

  async function loadSurah(number) {
    const output = $("ayahList");
    output.textContent = "Oyatlar yuklanmoqda...";

    try {
      const response = await fetch(
        `https://api.alquran.cloud/v1/surah/${number}`
      );

      if (!response.ok) throw new Error();

      const result = await response.json();
      const surah = result.data;

      output.innerHTML = `
        <div class="card">
          <h2>${escapeHTML(surah.englishName)} — ${escapeHTML(surah.name)}</h2>
          ${surah.ayahs.map((ayah) => `
            <div class="list-item">
              <div class="arabic">${escapeHTML(ayah.text)} ۞</div>
              <div class="muted">${ayah.numberInSurah}-oyat</div>
            </div>
          `).join("")}
        </div>`;
    } catch {
      output.textContent = "Oyatlarni yuklashda xatolik yuz berdi.";
    }
  }

  async function renderAudioSection() {
    const list = $("audioSurahList");

    try {
      const response = await fetch("https://api.alquran.cloud/v1/surah");
      if (!response.ok) throw new Error();

      const result = await response.json();

      list.innerHTML = result.data.map((surah) => `
        <div class="list-item row">
          <div>
            <b>${surah.number}. ${escapeHTML(surah.englishName)}</b>
            <div class="muted">${escapeHTML(surah.name)}</div>
          </div>
          <button type="button" data-audio-surah="${surah.number}">Tinglash</button>
        </div>
      `).join("");
    } catch {
      list.textContent = "Suralar ro‘yxatini yuklab bo‘lmadi.";
    }
  }

  async function playAudio(number) {
    const player = $("audioPlayer");
    const reciter = $("reciterSelect").value;

    player.textContent = "Audio yuklanmoqda...";

    try {
      const response = await fetch(
        `https://api.alquran.cloud/v1/surah/${number}/${encodeURIComponent(reciter)}`
      );

      if (!response.ok) throw new Error();

      const result = await response.json();
      const audioUrl = result.data?.ayahs?.[0]?.audio;

      if (!audioUrl) throw new Error();

      player.innerHTML = `
        <div class="card">
          <h3>${number}-sura</h3>
          <audio controls preload="none" src="${escapeHTML(audioUrl)}"></audio>
          <p class="muted">Audio fon rejimida ishlashi iPhone va brauzer tomonidan cheklanishi mumkin.</p>
        </div>`;
    } catch {
      player.textContent = "Audio manbasi topilmadi. Boshqa qori tanlab ko‘ring.";
    }
  }

  function renderAdhkar(section) {
    const title = section === "morning"
      ? "Tonggi zikrlar"
      : section === "evening"
        ? "Kechgi zikrlar"
        : "Tasbeh";

    $("adhkarList").innerHTML = `
      <p class="muted">${title}. Bu ro‘yxat hozircha 5 ta namunaviy zikrdan iborat.</p>
      ${adhkar.map((zikr, index) => {
        const key = `${section}-${index}`;
        const count = state.zikrCounts[key] || 0;

        return `
          <div class="card">
            <div class="row">
              <h3>${index + 1}. ${escapeHTML(zikr.title)}</h3>
              <span class="gold-text">${zikr.count}×</span>
            </div>
            <div class="arabic">${zikr.arabic}</div>
            <p>${escapeHTML(zikr.meaning)}</p>
            <p class="muted">${escapeHTML(zikr.source)}</p>
            <div class="counter" id="count-${key}">${count} / ${zikr.count}</div>
            <div class="actions">
              <button type="button" data-zikr="${key}">+1</button>
              <button type="button" data-reset-zikr="${key}">Qayta</button>
            </div>
          </div>`;
      }).join("")}
    `;
  }

  function changeZikr(key, reset = false) {
    const index = Number(key.split("-").at(-1));
    const target = adhkar[index]?.count || 33;

    state.zikrCounts[key] = reset
      ? 0
      : Math.min(target, (state.zikrCounts[key] || 0) + 1);

    const element = $(`count-${key}`);
    if (!element) return;

    element.textContent = `${state.zikrCounts[key]} / ${target}`;

    if (state.zikrCounts[key] === target) {
      element.style.color = "#64d98b";
    } else {
      element.style.color = "";
    }
  }

  function renderPrayerForm() {
    $("prayerForm").innerHTML = `
      <label for="cityInput">Shahar</label>
      <input class="field" id="cityInput" value="${escapeHTML(state.city)}">

      <label for="countryInput">Mamlakat</label>
      <input class="field" id="countryInput" value="${escapeHTML(state.country)}">

      <label for="methodInput">Hisoblash usuli</label>
      <select class="field" id="methodInput">
        <option value="3">Muslim World League</option>
        <option value="4">Umm al-Qura</option>
        <option value="1">Karachi</option>
      </select>

      <button class="gold-button" id="calculatePrayer" type="button">
        Namoz vaqtlarini olish
      </button>
    `;
  }

  async function fetchPrayerTimes() {
    const city = $("cityInput").value.trim();
    const country = $("countryInput").value.trim();
    const method = $("methodInput").value;
    const result = $("prayerResult");

    if (!city || !country) {
      result.textContent = "Shahar va mamlakatni kiriting.";
      return;
    }

    result.textContent = "Hisoblanmoqda...";

    try {
      const now = new Date();
      const date = [
        String(now.getDate()).padStart(2, "0"),
        String(now.getMonth() + 1).padStart(2, "0"),
        now.getFullYear()
      ].join("-");

      const url = new URL(
        `https://api.aladhan.com/v1/timingsByCity/${date}`
      );

      url.searchParams.set("city", city);
      url.searchParams.set("country", country);
      url.searchParams.set("method", method);

      const response = await fetch(url);
      if (!response.ok) throw new Error();

      const data = await response.json();
      if (data.code !== 200) throw new Error();

      const times = data.data.timings;
      const entries = [
        ["Bomdod", times.Fajr],
        ["Peshin", times.Dhuhr],
        ["Asr", times.Asr],
        ["Shom", times.Maghrib],
        ["Xufton", times.Isha]
      ];

      state.city = city;
      state.country = country;
      state.method = Number(method);

      $("cityLabel").textContent = `${city}, ${country}`;
      $("prayerTimes").innerHTML = entries.map(([name, time]) => `
        <div class="prayer">${name}<strong>${escapeHTML(time)}</strong></div>
      `).join("");

      result.innerHTML = `
        <div class="card">
          <h2>${escapeHTML(city)}, ${escapeHTML(country)}</h2>
          ${entries.map(([name, time]) => `
            <div class="list-item row">
              <span>${name}</span>
              <b class="gold-text">${escapeHTML(time)}</b>
            </div>
          `).join("")}
          <p class="muted">Mahalliy masjid jadvali bilan solishtiring.</p>
        </div>`;
    } catch {
      result.textContent = "Namoz vaqtlarini olishda xatolik yuz berdi.";
    }
  }

  function startQuiz() {
    state.quizQuestions = Array.from(
      { length: 50 },
      (_, index) => quizBank[index % quizBank.length]
    );

    state.quizIndex = 0;
    state.quizScore = 0;

    showQuestion();
  }

  function showQuestion() {
    const question = state.quizQuestions[state.quizIndex];
    if (!question) return;

    $("quizContainer").innerHTML = `
      <div class="card">
        <div class="row">
          <span class="gold-text">Savol ${state.quizIndex + 1}/50</span>
          <span>Ball: ${state.quizScore}</span>
        </div>
        <h2>${escapeHTML(question.q)}</h2>
        ${question.a.map((answer, index) => `
          <button class="field" type="button" data-answer="${index}">
            ${"ABCD"[index]}. ${escapeHTML(answer)}
          </button>
        `).join("")}
        <p class="muted">
          Eslatma: hozir 5 ta namuna savoli takrorlanadi.
          50 ta noyob, tekshirilgan savol bazasi hali kiritilmagan.
        </p>
      </div>`;
  }

  async function answerQuestion(index) {
    const question = state.quizQuestions[state.quizIndex];
    if (!question) return;

    if (index === question.correct) {
      state.quizScore += 20;
      alert("To‘g‘ri! +20 ball\n" + question.explanation);
    } else {
      alert(
        "Noto‘g‘ri javob.\nTo‘g‘ri javob: " +
        question.a[question.correct] +
        "\n" + question.explanation
      );
    }

    state.quizIndex += 1;

    if (state.quizIndex >= state.quizQuestions.length) {
      $("quizContainer").innerHTML = `
        <div class="card">
          <h2>Viktorina tugadi</h2>
          <p>Jami ball: <b class="gold-text">${state.quizScore}</b></p>
          <button class="gold-button" id="restartQuiz" type="button">
            Qayta o‘ynash
          </button>
        </div>`;

      await saveScore();
      return;
    }

    showQuestion();
  }

  async function saveScore() {
    const user = tg?.initDataUnsafe?.user;

    if (!user || !tg?.initData) {
      alert("Reytingga yozish uchun viktorinani Telegram Mini App ichida oching.");
      return;
    }

    try {
      await apiFetch("/api/score", {
        method: "POST",
        headers: apiHeaders(),
        body: JSON.stringify({
          init_data: tg.initData,
          name: user.first_name || "Foydalanuvchi",
          score: state.quizScore
        })
      });
    } catch (error) {
      alert("Ballni saqlab bo‘lmadi: " + error.message);
    }
  }

  async function loadRanking() {
    const output = $("rankingContainer");

    try {
      const result = await apiFetch("/api/ranking");
      const items = result.items || [];

      output.innerHTML = items.length
        ? items.map((user, index) => `
            <div class="list-item row">
              <b>${["🥇", "🥈", "🥉"][index] || `${index + 1}.`} ${escapeHTML(user.name)}</b>
              <span class="gold-text">${user.score} ball</span>
            </div>
          `).join("")
        : "Reytingda hozircha ma’lumot yo‘q.";
    } catch {
      output.textContent = "Reyting serveriga ulanib bo‘lmadi.";
    }
  }

  async function askAI() {
    const question = $("aiQuestion").value.trim();
    const output = $("aiAnswer");

    if (!question) {
      output.textContent = "Savolingizni yozing.";
      return;
    }

    if (!tg?.initData) {
      output.textContent = "TAQVO AI’ni Telegram Mini App ichida oching.";
      return;
    }

    output.textContent = "Javob tayyorlanmoqda...";

    try {
      const result = await apiFetch("/api/ask", {
        method: "POST",
        headers: apiHeaders(),
        body: JSON.stringify({
          init_data: tg.initData,
          question
        })
      });

      output.textContent = result.answer || "Javob olinmadi.";
    } catch (error) {
      output.textContent = error.message;
    }
  }

  async function checkSubscription() {
    const message = $("subscriptionMessage");

    if (!tg?.initData) {
      message.textContent = "Obunani tekshirish uchun Telegram Mini App ichida oching.";
      return;
    }

    message.textContent = "Obuna tekshirilmoqda...";

    try {
      const result = await apiFetch("/api/subscription", {
        method: "POST",
        headers: apiHeaders(),
        body: JSON.stringify({ init_data: tg.initData })
      });

      if (result.subscribed) {
        $("subscriptionGate").classList.add("hidden");
        $("homeScreen").classList.remove("hidden");
        message.textContent = "";
      } else {
        message.textContent = "Kanalga obuna bo‘lib, qayta tekshiring.";
      }
    } catch (error) {
      message.textContent = error.message;
    }
  }

  function toggleLanguage() {
    state.language = state.language === "uz" ? "cyrl" : "uz";

    $("languageButton").textContent =
      state.language === "uz" ? "Кирилл" : "Lotin";

    alert(
      "Til tanlovi o‘zgardi. To‘liq lotin-kirill tarjimasi hali qo‘shilmagan."
    );
  }

  document.addEventListener("click", (event) => {
    const target = event.target.closest("button");
    if (!target) return;

    if (target.dataset.open) showSection(target.dataset.open);
    if (target.dataset.surah) loadSurah(Number(target.dataset.surah));
    if (target.dataset.audioSurah) playAudio(Number(target.dataset.audioSurah));
    if (target.dataset.zikr) changeZikr(target.dataset.zikr);
    if (target.dataset.resetZikr) changeZikr(target.dataset.resetZikr, true);
    if (target.dataset.answer !== undefined) {
      answerQuestion(Number(target.dataset.answer));
    }

    if (target.id === "backButton") showHome();
    if (target.id === "calculatePrayer") fetchPrayerTimes();
    if (target.id === "askAIButton") askAI();
    if (target.id === "checkSubscription") checkSubscription();
    if (target.id === "restartQuiz") startQuiz();
  });

  $("languageButton").addEventListener("click", toggleLanguage);

  function init() {
    renderMenu();
    showHome();

    if (tg?.initData) {
      $("subscriptionGate").classList.remove("hidden");
      $("homeScreen").classList.add("hidden");
      checkSubscription();
    }
  }

  init();
})();
