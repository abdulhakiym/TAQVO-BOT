
/* =========================================================
   TAQVO PRO MAX — COMPLETE APPLICATION
   File: docs/js/app.js
   Version: 2.0
   Prayer calculation: Hanafi (fixed)
   Languages: Uzbek, Uzbek Cyrillic, Russian
   ========================================================= */

(() => {
  "use strict";

  /* =========================
     1. CONFIGURATION
  ========================= */

  const CONFIG = {
    API_BASE: "https://taqvo-api-uz.onrender.com",
    DEFAULT_LANGUAGE: "uz",
    DEFAULT_METHOD: 3,
    DEFAULT_TIMEZONE: "Asia/Almaty",
    SEARCH_DELAY: 350,
    REFRESH_INTERVAL: 60000
  };

  const STORAGE = {
    language: "taqvo_language",
    city: "taqvo_selected_city",
    settings: "taqvo_prayer_settings"
  };

  const PRAYERS = [
    { id: "fajr", key: "fajr", names: { uz: "Bomdod", "uz-Cyrl": "Бомдод", ru: "Фаджр" } },
    { id: "dhuhr", key: "dhuhr", names: { uz: "Peshin", "uz-Cyrl": "Пешин", ru: "Зухр" } },
    { id: "asr", key: "asr", names: { uz: "Asr", "uz-Cyrl": "Аср", ru: "Аср" } },
    { id: "maghrib", key: "maghrib", names: { uz: "Shom", "uz-Cyrl": "Шом", ru: "Магриб" } },
    { id: "isha", key: "isha", names: { uz: "Xufton", "uz-Cyrl": "Хуфтон", ru: "Иша" } }
  ];

  /* =========================
     2. TRANSLATIONS
  ========================= */

  const TRANSLATIONS = {
    uz: {
      home: "Bosh sahifa",
      quran: "Qur’oni Karim",
      prayer: "Namoz vaqtlari",
      tasbeeh: "Tasbeh",
      morning: "Tonggi zikrlar",
      evening: "Kechki zikrlar",
      duas: "Duolar",
      hadith: "Hadislar",
      quiz: "TAQVO QUIZ",
      ai: "TAQVO AI",
      selectCity: "Shaharni tanlang",
      searchCity: "Shahar nomini yozing...",
      cityNotFound: "Shahar topilmadi",
      loading: "Yuklanmoqda...",
      connectionError: "Server bilan bog‘lanishda xatolik",
      location: "Joylashuv",
      today: "Bugun",
      nextPrayer: "Keyingi namoz",
      calculationMethod: "Hisoblash usuli",
      settings: "Sozlamalar",
      saved: "Saqlandi",
      retry: "Qayta urinish",
      noCity: "Avval shaharni tanlang",
      chooseCity: "Shaharni tanlash",
      close: "Yopish"
    },

    "uz-Cyrl": {
      home: "Бош саҳифа",
      quran: "Қуръони Карим",
      prayer: "Намоз вақтлари",
      tasbeeh: "Тасбеҳ",
      morning: "Тонгги зикрлар",
      evening: "Кечки зикрлар",
      duas: "Дуолар",
      hadith: "Ҳадислар",
      quiz: "TAQVO QUIZ",
      ai: "TAQVO AI",
      selectCity: "Шаҳарни танланг",
      searchCity: "Шаҳар номини ёзинг...",
      cityNotFound: "Шаҳар топилмади",
      loading: "Юкланмоқда...",
      connectionError: "Сервер билан боғланишда хатолик",
      location: "Жойлашув",
      today: "Бугун",
      nextPrayer: "Кейинги намоз",
      calculationMethod: "Ҳисоблаш усули",
      settings: "Созламалар",
      saved: "Сақланди",
      retry: "Қайта уриниш",
      noCity: "Аввал шаҳарни танланг",
      chooseCity: "Шаҳарни танлаш",
      close: "Ёпиш"
    },

    ru: {
      home: "Главная",
      quran: "Священный Коран",
      prayer: "Время намаза",
      tasbeeh: "Тасбих",
      morning: "Утренние азкары",
      evening: "Вечерние азкары",
      duas: "Дуа",
      hadith: "Хадисы",
      quiz: "TAQVO QUIZ",
      ai: "TAQVO AI",
      selectCity: "Выберите город",
      searchCity: "Введите название города...",
      cityNotFound: "Город не найден",
      loading: "Загрузка...",
      connectionError: "Ошибка соединения с сервером",
      location: "Местоположение",
      today: "Сегодня",
      nextPrayer: "Следующий намаз",
      calculationMethod: "Метод расчёта",
      settings: "Настройки",
      saved: "Сохранено",
      retry: "Повторить",
      noCity: "Сначала выберите город",
      chooseCity: "Выбрать город",
      close: "Закрыть"
    }
  };

  /* =========================
     3. STATE
  ========================= */

  let language = localStorage.getItem(STORAGE.language) || CONFIG.DEFAULT_LANGUAGE;
  let selectedCity = readJSON(STORAGE.city, null);

  let prayerSettings = readJSON(STORAGE.settings, {
    method: CONFIG.DEFAULT_METHOD,
    madhhab: "hanafi"
  });

  // Hanafi is fixed. The user cannot change madhhab.
  prayerSettings.madhhab = "hanafi";

  let prayerData = null;
  let countdownTimer = null;
  let searchTimer = null;
  let lastCountdownValue = "";
  let citySearchRequest = 0;

  /* =========================
     4. HELPERS
  ========================= */

  function readJSON(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      console.warn("TAQVO storage error:", error);
      return fallback;
    }
  }

  function saveJSON(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.warn("TAQVO save error:", error);
    }
  }

  function t(key) {
    const dictionary = TRANSLATIONS[language] || TRANSLATIONS.uz;
    return dictionary[key] || TRANSLATIONS.uz[key] || key;
  }

  function normalizeLanguage(value) {
    if (value === "uz-Cyrl" || value === "ru") return value;
    return "uz";
  }

  function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    })[char]);
  }

  function pad(number) {
    return String(number).padStart(2, "0");
  }

  function getTimezone() {
    return selectedCity?.timezone ||
      prayerSettings.timezone ||
      CONFIG.DEFAULT_TIMEZONE;
  }

  function showToast(message) {
    let toast = document.getElementById("taqvoToast");

    if (!toast) {
      toast = document.createElement("div");
      toast.id = "taqvoToast";
      document.body.appendChild(toast);
    }

    toast.textContent = message;
    toast.classList.add("show");

    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.classList.remove("show");
    }, 2600);
  }

  function setLoading(element, message = null) {
    if (!element) return;

    element.textContent = message || t("loading");
  }

  async function apiRequest(path, options = {}) {
    const response = await fetch(CONFIG.API_BASE + path, {
      ...options,
      headers: {
        Accept: "application/json",
        ...(options.headers || {})
      }
    });

    if (!response.ok) {
      throw new Error("API error: " + response.status);
    }

    return response.json();
  }

  /* =========================
     5. TELEGRAM WEB APP
  ========================= */

  function initTelegram() {
    const telegram = window.TeleGRAM?.WebApp;

    if (!telegram) return;

    try {
      telegram.ready();
      telegram.expand();

      if (telegram.setHeaderColor) {
        telegram.setHeaderColor("#050507");
      }

      if (telegram.setBackgroundColor) {
        telegram.setBackgroundColor("#050507");
      }

      window.TAQVO_TELEGRAM = telegram;
      window.TAQVO_USER = telegram.initDataUnsafe?.user || null;
    } catch (error) {
      console.warn("Telegram initialization error:", error);
    }
  }

  /* =========================
     6. LANGUAGE SYSTEM
  ========================= */

  function applyLanguage() {
    document.documentElement.lang =
      language === "uz-Cyrl" ? "uz" : language;

    document.querySelectorAll("[data-i18n]").forEach(element => {
      const key = element.dataset.i18n;
      const translated = t(key);

      if (translated) element.textContent = translated;
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(element => {
      element.placeholder = t(element.dataset.i18nPlaceholder);
    });

    const languageSelect = document.getElementById("languageSelect");

    if (languageSelect) {
      languageSelect.value = language;
    }

    renderPrayerNames();
    updateCityDates();
  }

  function changeLanguage(value) {
    language = normalizeLanguage(value);

    localStorage.setItem(STORAGE.language, language);

    applyLanguage();

    if (selectedCity) {
      loadPrayerTimes();
    }
  }

  function initLanguage() {
    language = normalizeLanguage(language);

    const select = document.getElementById("languageSelect");

    if (select) {
      select.value = language;

      select.addEventListener("change", event => {
        changeLanguage(event.target.value);
      });
    }

    applyLanguage();
  }

  /* =========================
     7. NAVIGATION
  ========================= */

  function initNavigation() {
    document.addEventListener("click", event => {
      const link = event.target.closest("[data-section], [data-page]");

      if (!link) return;

      const section =
        link.dataset.section ||
        link.dataset.page;

      if (!section) return;

      const target = document.getElementById(section);

      if (!target) return;

      event.preventDefault();

      document.querySelectorAll(".page, .app-section").forEach(page => {
        page.classList.remove("active");
      });

      target.classList.add("active");

      document.querySelectorAll("[data-section], [data-page]").forEach(item => {
        item.classList.remove("active");
      });

      link.classList.add("active");

      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    });
  }

  /* =========================
     8. CITY MODAL
  ========================= */

  function createCityModal() {
    if (document.getElementById("taqvoCityModal")) return;

    const modal = document.createElement("div");

    modal.id = "taqvoCityModal";
    modal.innerHTML = `
      <div class="taqvo-city-backdrop"></div>
      <div class="taqvo-city-dialog">
        <div class="taqvo-city-header">
          <strong>${escapeHTML(t("selectCity"))}</strong>
          <button type="button" id="taqvoCityClose">✕</button>
        </div>
        <input
          id="taqvoCitySearch"
          type="search"
          placeholder="${escapeHTML(t("searchCity"))}"
          autocomplete="off"
        />
        <div id="taqvoCityResults">
          <div class="taqvo-city-empty">${escapeHTML(t("searchCity"))}</div>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const style = document.createElement("style");

    style.id = "taqvoCityModalStyles";
    style.textContent = `
      #taqvoCityModal {
        display:none;
        position:fixed;
        inset:0;
        z-index:99999;
        font-family:inherit;
      }
      #taqvoCityModal.open { display:block; }
      .taqvo-city-backdrop {
        position:absolute;
        inset:0;
        background:rgba(0,0,0,.78);
        backdrop-filter:blur(7px);
      }
      .taqvo-city-dialog {
        position:absolute;
        left:50%;
        top:50%;
        transform:translate(-50%,-50%);
        width:calc(100% - 32px);
        max-width:420px;
        max-height:80vh;
        overflow:hidden;
        padding:20px;
        border:1px solid rgba(255,190,65,.35);
        border-radius:20px;
        background:#101014;
        color:#fff;
        box-shadow:0 15px 60px rgba(0,0,0,.5);
      }
      .taqvo-city-header {
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:12px;
        margin-bottom:16px;
        color:#ffd36a;
      }
      #taqvoCityClose {
        border:0;
        background:transparent;
        color:#fff;
        font-size:22px;
        padding:4px 8px;
      }
      #taqvoCitySearch {
        width:100%;
        box-sizing:border-box;
        padding:14px;
        border-radius:12px;
        border:1px solid #454047;
        outline:none;
        background:#1b1a20;
        color:#fff;
        font-size:16px;
      }
      #taqvoCityResults {
        overflow-y:auto;
        max-height:50vh;
        margin-top:12px;
      }
      .taqvo-city-result {
        width:100%;
        display:block;
        padding:13px 12px;
        margin:5px 0;
        border:1px solid #302d31;
        border-radius:10px;
        background:#19181d;
        color:#fff;
        text-align:left;
        font-size:15px;
      }
      .taqvo-city-result:active {
        background:#493719;
      }
      .taqvo-city-empty {
        padding:16px 5px;
        color:#aaa;
        text-align:center;
      }
      #taqvoToast {
        position:fixed;
        z-index:100000;
        bottom:28px;
        left:50%;
        transform:translate(-50%,20px);
        opacity:0;
        pointer-events:none;
        padding:12px 18px;
        border-radius:12px;
        background:#242126;
        color:#fff;
        border:1px solid rgba(255,190,65,.4);
        transition:.2s ease;
        max-width:85%;
        text-align:center;
      }
      #taqvoToast.show {
        opacity:1;
        transform:translate(-50%,0);
      }
    `;

    document.head.appendChild(style);

    document.getElementById("taqvoCityClose")
      .addEventListener("click", closeCityModal);

    modal.querySelector(".taqvo-city-backdrop")
      .addEventListener("click", closeCityModal);

    document.getElementById("taqvoCitySearch")
      .addEventListener("input", handleCitySearch);
  }

  function openCityModal() {
    createCityModal();

    const modal = document.getElementById("taqvoCityModal");
    const input = document.getElementById("taqvoCitySearch");

    modal.classList.add("open");

    input.value = "";
    input.focus();

    document.getElementById("taqvoCityResults").innerHTML =
      `<div class="taqvo-city-empty">${escapeHTML(t("searchCity"))}</div>`;
  }

  function closeCityModal() {
    document.getElementById("taqvoCityModal")?.classList.remove("open");
  }

  /* =========================
     9. CITY SEARCH
  ========================= */

  function handleCitySearch(event) {
    const query = event.target.value.trim();

    clearTimeout(searchTimer);

    if (query.length < 2) {
      document.getElementById("taqvoCityResults").innerHTML =
        `<div class="taqvo-city-empty">${escapeHTML(t("searchCity"))}</div>`;
      return;
    }

    searchTimer = setTimeout(() => {
      searchCities(query);
    }, CONFIG.SEARCH_DELAY);
  }

  async function searchCities(query) {
    const resultsElement = document.getElementById("taqvoCityResults");
    const requestId = ++citySearchRequest;

    setLoading(resultsElement);

    try {
      const params = new URLSearchParams({
        q: query,
        count: "15",
        language: language
      });

      const data = await apiRequest(
        `/api/prayer/cities?${params.toString()}`
      );

      if (requestId !== citySearchRequest) return;

      const cities = Array.isArray(data)
        ? data
        : data.cities || data.results || data.data || [];

      if (!cities.length) {
        resultsElement.innerHTML =
          `<div class="taqvo-city-empty">${escapeHTML(t("cityNotFound"))}</div>`;
        return;
      }

      resultsElement.innerHTML = "";

      cities.forEach(city => {
        const button = document.createElement("button");

        button.type = "button";
        button.className = "taqvo-city-result";

        const name =
          city.name ||
          city.city ||
          city.display_name ||
          city.name_ru ||
          "Unknown";

        const country = city.country || city.country_name || "";

        button.textContent = country ? `${name}, ${country}` : name;

        button.addEventListener("click", () => {
          selectCity(city);
        });

        resultsElement.appendChild(button);
      });

    } catch (error) {
      console.error("City search error:", error);

      if (requestId !== citySearchRequest) return;

      resultsElement.innerHTML =
        `<div class="taqvo-city-empty">${escapeHTML(t("connectionError"))}</div>`;
    }
  }

  function normalizeCity(city) {
    const latitude = Number(
      city.latitude ?? city.lat ?? city.location?.latitude
    );

    const longitude = Number(
      city.longitude ?? city.lon ?? city.lng ?? city.location?.longitude
    );

    return {
      name: city.name || city.city || city.display_name || "Unknown",
      country: city.country || city.country_name || "",
      latitude,
      longitude,
      timezone: city.timezone || city.time_zone || CONFIG.DEFAULT_TIMEZONE
    };
  }

  async function selectCity(rawCity) {
    const city = normalizeCity(rawCity);

    if (
      !Number.isFinite(city.latitude) ||
      !Number.isFinite(city.longitude)
    ) {
      showToast(t("connectionError"));
      console.error("Invalid city coordinates:", rawCity);
      return;
    }

    selectedCity = city;

    prayerSettings.timezone = city.timezone;

    saveJSON(STORAGE.city, selectedCity);
    saveJSON(STORAGE.settings, prayerSettings);

    closeCityModal();

    updateCityName();
    updateCityDates();

    await loadPrayerTimes();
  }

  function updateCityName() {
    const cityName = selectedCity
      ? [selectedCity.name, selectedCity.country].filter(Boolean).join(", ")
      : t("chooseCity");

    const selectors = [
      "#userLocation",
      "#selectedCity",
      "[data-selected-city]"
    ];

    selectors.forEach(selector => {
      document.querySelectorAll(selector).forEach(element => {
        element.textContent = cityName;
      });
    });
  }

  /* =========================
     10. DATE AND TIME
  ========================= */

  function getCityDate() {
    try {
      return new Date(
        new Date().toLocaleString("en-US", {
          timeZone: getTimezone()
        })
      );
    } catch {
      return new Date();
    }
  }

  function updateCityDates() {
    const now = getCityDate();

    const gregorian = new Intl.DateTimeFormat(
      language === "ru" ? "ru-RU" :
      language === "uz-Cyrl" ? "uz-UZ" : "uz-UZ",
      {
        day: "numeric",
        month: "long",
        year: "numeric",
        timeZone: getTimezone()
      }
    ).format(new Date());

    const gregorianElement = document.getElementById("gregorianDate");

    if (gregorianElement) {
      gregorianElement.textContent = gregorian;
    }

    const cityClock = document.getElementById("cityClock");

    if (cityClock) {
      cityClock.textContent =
        `${pad(now.getHours())}:${pad(now.getMinutes())}`;
    }

    if (prayerData?.hijri) {
      const hijriElement = document.getElementById("hijriDate");

      if (hijriElement) {
        const hijri = prayerData.hijri;

        hijriElement.textContent =
          hijri.date ||
          [hijri.day, hijri.month?.en || hijri.month, hijri.year]
            .filter(Boolean)
            .join(" ");
      }
    }
  }

  /* =========================
     11. PRAYER SETTINGS
  ========================= */

  function getPrayerSettings() {
    return {
      method: Number(prayerSettings.method || CONFIG.DEFAULT_METHOD),
      madhhab: "hanafi",
      timezone: getTimezone()
    };
  }

  function savePrayerSettings() {
    prayerSettings.madhhab = "hanafi";
    saveJSON(STORAGE.settings, prayerSettings);
  }

  function openPrayerSettings() {
    const current = getPrayerSettings();

    const answer = window.prompt(
      language === "ru"
        ? "Введите номер метода расчёта (по умолчанию 3):"
        : "Hisoblash usuli raqamini kiriting (standart 3):",
      String(current.method)
    );

    if (answer === null) return;

    const method = Number(answer);

    if (!Number.isInteger(method) || method < 0 || method > 99) {
      showToast(t("connectionError"));
      return;
    }

    prayerSettings.method = method;
    prayerSettings.madhhab = "hanafi";

    savePrayerSettings();
    loadPrayerTimes();
  }

  /* =========================
     12. LOAD PRAYER TIMES
  ========================= */

  async function loadPrayerTimes() {
    if (!selectedCity) {
      updateCityName();
      return;
    }

    const params = new URLSearchParams({
      latitude: String(selectedCity.latitude),
      longitude: String(selectedCity.longitude),
      timezone: getTimezone(),
      method: String(getPrayerSettings().method),
      madhhab: "hanafi"
    });

    try {
      const data = await apiRequest(
        `/api/prayer/today?${params.toString()}`
      );

      if (data.success === false) {
        throw new Error(data.message || "Prayer API error");
      }

      prayerData = data;

      renderPrayerTimes();
      renderPrayerNames();
      updateCityDates();
      updateNextPrayer();

      document.dispatchEvent(
        new CustomEvent("taqvo:prayer-loaded", {
          detail: data
        })
      );

    } catch (error) {
      console.error("Prayer loading error:", error);
      showToast(t("connectionError"));
    }
  }

  /* =========================
     13. RENDER PRAYER TIMES
  ========================= */

  function normalizePrayerTime(value) {
    if (!value) return "--:--";

    const match = String(value).match(/(\d{1,2}):(\d{2})/);

    if (!match) return "--:--";

    return `${pad(Number(match[1]))}:${match[2]}`;
  }

  function renderPrayerTimes() {
    if (!prayerData?.timings) return;

    PRAYERS.forEach(prayer => {
      const time = normalizePrayerTime(
        prayerData.timings[prayer.key]
      );

      const card = document.querySelector(
        `.prayer-item[data-prayer="${prayer.id}"]`
      );

      if (!card) return;

      const timeElement =
        card.querySelector(".prayer-time") ||
        card.querySelector("[data-prayer-time]") ||
        card.querySelector(".time");

      if (timeElement) {
        timeElement.textContent = time;
      } else {
        const existing = card.querySelector("span:last-child");

        if (existing) existing.textContent = time;
      }

      card.dataset.time = time;
    });
  }

  function renderPrayerNames() {
    PRAYERS.forEach(prayer => {
      const card = document.querySelector(
        `.prayer-item[data-prayer="${prayer.id}"]`
      );

      if (!card) return;

      const nameElement =
        card.querySelector(".prayer-name") ||
        card.querySelector("[data-prayer-name]");

      if (nameElement) {
        nameElement.textContent =
          prayer.names[language] || prayer.names.uz;
      }
    });
  }

  /* =========================
     14. NEXT PRAYER COUNTDOWN
  ========================= */

  function parsePrayerDate(time, baseDate) {
    const normalized = normalizePrayerTime(time);

    if (normalized === "--:--") return null;

    const [hours, minutes] = normalized.split(":").map(Number);

    const date = new Date(baseDate);

    date.setHours(hours, minutes, 0, 0);

    return date;
  }

  function updateNextPrayer() {
    if (!prayerData?.timings) return;

    const now = getCityDate();

    const schedule = PRAYERS.map(prayer => ({
      ...prayer,
      time: normalizePrayerTime(
        prayerData.timings[prayer.key]
      )
    }));

    let next = null;

    for (const prayer of schedule) {
      const date = parsePrayerDate(prayer.time, now);

      if (date && date > now) {
        next = { ...prayer, date };
        break;
      }
    }

    if (!next) {
      const tomorrow = new Date(now);
      tomorrow.setDate(tomorrow.getDate() + 1);

      const first = schedule[0];
      const date = parsePrayerDate(first.time, tomorrow);

      if (date) next = { ...first, date };
    }

    document.querySelectorAll(".prayer-item").forEach(card => {
      card.classList.remove("active", "next-prayer");
    });

    if (!next) return;

    const activeCard = document.querySelector(
      `.prayer-item[data-prayer="${next.id}"]`
    );

    if (activeCard) {
      activeCard.classList.add("active", "next-prayer");
    }

    const nameElement = document.getElementById("nextPrayerName");
    const countdownElement = document.getElementById("nextPrayerCountdown");

    if (nameElement) {
      nameElement.textContent =
        next.names[language] || next.names.uz;
    }

    if (countdownElement) {
      const difference = Math.max(
        0,
        Math.floor((next.date - now) / 1000)
      );

      const hours = Math.floor(difference / 3600);
      const minutes = Math.floor((difference % 3600) / 60);
      const seconds = difference % 60;

      const value = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;

      if (lastCountdownValue !== value) {
        countdownElement.textContent = value;
        lastCountdownValue = value;
      }
    }
  }

  /* =========================
     15. CITY AND PRAYER EVENTS
  ========================= */

  function initCityAndPrayer() {
    createCityModal();

    document.addEventListener("click", event => {
      const cityButton = event.target.closest(
        '[data-action="select-city"], #userLocation, #selectedCity'
      );

      if (cityButton) {
        event.preventDefault();
        openCityModal();
        return;
      }

      const settingsButton = event.target.closest(
        '[data-action="prayer-settings"]'
      );

      if (settingsButton) {
        event.preventDefault();
        openPrayerSettings();
      }
    });

    updateCityName();

    if (selectedCity) {
      loadPrayerTimes();
    }

    if (!countdownTimer) {
      countdownTimer = setInterval(() => {
        updateNextPrayer();
        updateCityDates();
      }, 1000);
    }
  }

  /* =========================
     16. GLOBAL APP API
  ========================= */

  window.TAQVO = {
    version: "2.0.0",

    get language() {
      return language;
    },

    get city() {
      return selectedCity;
    },

    get prayerData() {
      return prayerData;
    },

    t,
    showToast,
    changeLanguage,
    openCityModal,
    closeCityModal,
    selectCity,
    loadPrayerTimes,
    openPrayerSettings,
    updateNextPrayer,

    getPrayerSettings,

    setCity(city) {
      return selectCity(city);
    }
  };

  /* =========================
     17. INITIALIZATION
  ========================= */

  function init() {
    initTelegram();
    initLanguage();
    initNavigation();
    initCityAndPrayer();

    document.dispatchEvent(
      new CustomEvent("taqvo:ready")
    );

    console.log(
      "%c TAQVO PRO MAX ",
      "background:#111;color:#ffd700;font-weight:bold;padding:8px;"
    );

    console.log("TAQVO application initialized.");
    console.log("Prayer madhhab: Hanafi (fixed).");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }

})();
