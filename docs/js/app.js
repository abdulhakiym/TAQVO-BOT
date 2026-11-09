/* =========================================================
   TAQVO PRO MAX — APPLICATION
   File: docs/js/app.js
   Version: 2.1.0
   Prayer calculation: Hanafi fixed (no madhhab selector)
   Languages: Uzbek Latin, Uzbek Cyrillic, Russian
   ========================================================= */

(() => {
  "use strict";

  const CONFIG = {
    API_BASE: "https://taqvo-api-uz.onrender.com",
    DEFAULT_LANGUAGE: "uz",
    DEFAULT_METHOD: 3,
    DEFAULT_TIMEZONE: "Asia/Almaty",
    SEARCH_DELAY: 350,
    CACHE_REFRESH_INTERVAL: 60000
  };

  const STORAGE = {
    language: "taqvo_language",
    city: "taqvo_selected_city",
    settings: "taqvo_prayer_settings",
    prayerCache: "taqvo_prayer_cache_v1"
  };

  const PRAYERS = [
    { id: "fajr", key: "fajr", names: { uz: "Bomdod", "uz-Cyrl": "Бомдод", ru: "Фаджр" } },
    { id: "dhuhr", key: "dhuhr", names: { uz: "Peshin", "uz-Cyrl": "Пешин", ru: "Зухр" } },
    { id: "asr", key: "asr", names: { uz: "Asr", "uz-Cyrl": "Аср", ru: "Аср" } },
    { id: "maghrib", key: "maghrib", names: { uz: "Shom", "uz-Cyrl": "Шом", ru: "Магриб" } },
    { id: "isha", key: "isha", names: { uz: "Xufton", "uz-Cyrl": "Хуфтон", ru: "Иша" } }
  ];

  const TRANSLATIONS = {
    uz: {
      home: "Bosh sahifa", quran: "Qur’oni Karim", prayer: "Namoz vaqtlari",
      tasbeeh: "Tasbeh", morning: "Tonggi zikrlar", evening: "Kechki zikrlar",
      duas: "Duolar", hadith: "Hadislar", quiz: "TAQVO QUIZ", ai: "TAQVO AI",
      selectCity: "Shaharni tanlang", searchCity: "Shahar nomini yozing...",
      cityNotFound: "Shahar topilmadi", loading: "Yuklanmoqda...",
      connectionError: "Server bilan bog‘lanishda xatolik", location: "Joylashuv",
      today: "Bugun", nextPrayer: "Keyingi namoz", calculationMethod: "Hisoblash usuli",
      settings: "Sozlamalar", saved: "Saqlandi", retry: "Qayta urinish",
      noCity: "Avval shaharni tanlang", chooseCity: "Shaharni tanlash", close: "Yopish",
      offlineCache: "Internet yo‘q. Saqlangan bugungi namoz vaqtlari ko‘rsatildi."
    },
    "uz-Cyrl": {
      home: "Бош саҳифа", quran: "Қуръони Карим", prayer: "Намоз вақтлари",
      tasbeeh: "Тасбеҳ", morning: "Тонгги зикрлар", evening: "Кечки зикрлар",
      duas: "Дуолар", hadith: "Ҳадислар", quiz: "TAQVO QUIZ", ai: "TAQVO AI",
      selectCity: "Шаҳарни танланг", searchCity: "Шаҳар номини ёзинг...",
      cityNotFound: "Шаҳар топилмади", loading: "Юкланмоқда...",
      connectionError: "Сервер билан боғланишда хатолик", location: "Жойлашув",
      today: "Бугун", nextPrayer: "Кейинги намоз", calculationMethod: "Ҳисоблаш усули",
      settings: "Созламалар", saved: "Сақланди", retry: "Қайта уриниш",
      noCity: "Аввал шаҳарни танланг", chooseCity: "Шаҳарни танлаш", close: "Ёпиш",
      offlineCache: "Интернет йўқ. Сақланган бугунги намоз вақтлари кўрсатилди."
    },
    ru: {
      home: "Главная", quran: "Священный Коран", prayer: "Время намаза",
      tasbeeh: "Тасбих", morning: "Утренние азкары", evening: "Вечерние азкары",
      duas: "Дуа", hadith: "Хадисы", quiz: "TAQVO QUIZ", ai: "TAQVO AI",
      selectCity: "Выберите город", searchCity: "Введите название города...",
      cityNotFound: "Город не найден", loading: "Загрузка...",
      connectionError: "Ошибка соединения с сервером", location: "Местоположение",
      today: "Сегодня", nextPrayer: "Следующий намаз", calculationMethod: "Метод расчёта",
      settings: "Настройки", saved: "Сохранено", retry: "Повторить",
      noCity: "Сначала выберите город", chooseCity: "Выбрать город", close: "Закрыть",
      offlineCache: "Нет интернета. Показано сохранённое время намаза на сегодня."
    }
  };

  /* -------------------------
     State and safe storage
  ------------------------- */

  function readJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (error) {
      console.warn("TAQVO storage read error:", error);
      return fallback;
    }
  }

  function saveJSON(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.warn("TAQVO storage write error:", error);
      return false;
    }
  }

  function normalizeLanguage(value) {
    return value === "uz-Cyrl" || value === "ru" ? value : "uz";
  }

  let language = normalizeLanguage(
    localStorage.getItem(STORAGE.language) || CONFIG.DEFAULT_LANGUAGE
  );
  let selectedCity = readJSON(STORAGE.city, null);
  let prayerSettings = readJSON(STORAGE.settings, {
    method: CONFIG.DEFAULT_METHOD,
    timezone: CONFIG.DEFAULT_TIMEZONE
  });

  if (!prayerSettings || typeof prayerSettings !== "object") {
    prayerSettings = { method: CONFIG.DEFAULT_METHOD, timezone: CONFIG.DEFAULT_TIMEZONE };
  }
  prayerSettings.method = Number.isInteger(Number(prayerSettings.method))
    ? Number(prayerSettings.method)
    : CONFIG.DEFAULT_METHOD;
  prayerSettings.madhhab = "hanafi";

  let prayerData = null;
  let countdownTimer = null;
  let searchTimer = null;
  let citySearchRequest = 0;
  let prayerRequestId = 0;
  let lastCountdownValue = "";
  let lastPrayerDateKey = "";

  /* -------------------------
     General helpers
  ------------------------- */

  function t(key) {
    return (TRANSLATIONS[language] || TRANSLATIONS.uz)[key] ||
      TRANSLATIONS.uz[key] || key;
  }

  function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    })[char]);
  }

  function pad(value) {
    return String(value).padStart(2, "0");
  }

  function getTimezone() {
    return selectedCity?.timezone || prayerSettings.timezone || CONFIG.DEFAULT_TIMEZONE;
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
    toast._timer = setTimeout(() => toast.classList.remove("show"), 2800);
  }

  function setLoading(element, message) {
    if (element) element.textContent = message || t("loading");
  }

  async function apiRequest(path, options = {}) {
    const response = await fetch(CONFIG.API_BASE + path, {
      ...options,
      headers: { Accept: "application/json", ...(options.headers || {}) }
    });
    if (!response.ok) throw new Error(`API error: ${response.status}`);
    return response.json();
  }

  function validCity(city) {
    if (!city) return false;
    const lat = Number(city.latitude);
    const lon = Number(city.longitude);
    return Number.isFinite(lat) && Number.isFinite(lon) &&
      lat >= -90 && lat <= 90 && lon >= -180 && lon <= 180;
  }

  /* -------------------------
     Correct city-local date/time
  ------------------------- */

  function getZonedParts(date = new Date()) {
    const parts = new Intl.DateTimeFormat("en-GB", {
      timeZone: getTimezone(),
      year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit",
      hourCycle: "h23"
    }).formatToParts(date);

    const values = {};
    parts.forEach(part => {
      if (part.type !== "literal") values[part.type] = Number(part.value);
    });
    return values;
  }

  // A city-local wall-clock Date. Used only for comparing prayer clock times.
  function getCityDate() {
    try {
      const p = getZonedParts();
      return new Date(p.year, p.month - 1, p.day, p.hour, p.minute, p.second);
    } catch (error) {
      console.warn("Timezone error:", getTimezone(), error);
      return new Date();
    }
  }

  function getCityDateKey() {
    try {
      const p = getZonedParts();
      return `${p.year}-${pad(p.month)}-${pad(p.day)}`;
    } catch {
      const d = new Date();
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
    }
  }

  function updateCityDates() {
    const dateElement = document.getElementById("gregorianDate");
    if (dateElement) {
      try {
        dateElement.textContent = new Intl.DateTimeFormat(
          language === "ru" ? "ru-RU" : "uz-UZ",
          { day: "numeric", month: "long", year: "numeric", timeZone: getTimezone() }
        ).format(new Date());
      } catch (error) {
        console.warn("Date formatting error:", error);
      }
    }

    const clockElement = document.getElementById("cityClock");
    if (clockElement) {
      const now = getCityDate();
      clockElement.textContent = `${pad(now.getHours())}:${pad(now.getMinutes())}`;
    }

    const hijriElement = document.getElementById("hijriDate");
    if (hijriElement && prayerData?.hijri) {
      const h = prayerData.hijri;
      hijriElement.textContent = h.date ||
        [h.day, h.month?.en || h.month, h.year].filter(Boolean).join(" ");
    }
  }

  /* -------------------------
     Prayer cache
     Saved per city, local date and calculation method.
  ------------------------- */

  function getPrayerCacheKey() {
    if (!selectedCity) return null;
    return [
      Number(selectedCity.latitude).toFixed(4),
      Number(selectedCity.longitude).toFixed(4),
      getTimezone(),
      getCityDateKey(),
      getPrayerSettings().method
    ].join("|");
  }

  function savePrayerCache(data) {
    if (!data?.timings || !selectedCity) return;
    saveJSON(STORAGE.prayerCache, {
      key: getPrayerCacheKey(),
      timings: data.timings,
      hijri: data.hijri || null,
      cachedAt: new Date().toISOString()
    });
  }

  function restorePrayerCache() {
    if (!selectedCity) return false;
    const cache = readJSON(STORAGE.prayerCache, null);
    if (!cache || cache.key !== getPrayerCacheKey() ||
        !cache.timings || typeof cache.timings !== "object") return false;

    prayerData = {
      timings: cache.timings,
      hijri: cache.hijri || null,
      cached: true,
      cachedAt: cache.cachedAt || null
    };
    renderPrayerTimes();
    renderPrayerNames();
    updateCityDates();
    updateNextPrayer();
    return true;
  }

  /* -------------------------
     Telegram Web App
  ------------------------- */

  function initTelegram() {
    const telegram = window.TELEGRAM?.WebApp;
    if (!telegram) return;
    try {
      telegram.ready();
      telegram.expand();
      telegram.setHeaderColor?.("#050507");
      telegram.setBackgroundColor?.("#050507");
      window.TAQVO_TELEGRAM = telegram;
      window.TAQVO_USER = telegram.initDataUnsafe?.user || null;
    } catch (error) {
      console.warn("Telegram initialization error:", error);
    }
  }

  /* -------------------------
     Language
  ------------------------- */

  function applyLanguage() {
    document.documentElement.lang = language === "uz-Cyrl" ? "uz" : language;
    document.documentElement.dir = "ltr";

    document.querySelectorAll("[data-i18n]").forEach(element => {
      element.textContent = t(element.dataset.i18n);
    });
    document.querySelectorAll("[data-i18n-placeholder]").forEach(element => {
      element.placeholder = t(element.dataset.i18nPlaceholder);
    });

    const select = document.getElementById("languageSelect");
    if (select) select.value = language;

    const search = document.getElementById("taqvoCitySearch");
    if (search) search.placeholder = t("searchCity");

    const title = document.querySelector("#taqvoCityModal .taqvo-city-header strong");
    if (title) title.textContent = t("selectCity");

    renderPrayerNames();
    updateCityName();
    updateCityDates();
  }

  function changeLanguage(value) {
    language = normalizeLanguage(value);
    try {
      localStorage.setItem(STORAGE.language, language);
    } catch (error) {
      console.warn("Language save error:", error);
    }
    applyLanguage();
    document.dispatchEvent(new CustomEvent("taqvo:language-changed", {
      detail: { language }
    }));
  }

  function initLanguage() {
    const select = document.getElementById("languageSelect");
    if (select) {
      select.value = language;
      select.addEventListener("change", event => changeLanguage(event.target.value));
    }
    applyLanguage();
  }

  /* -------------------------
     Navigation
  ------------------------- */

  function initNavigation() {
    document.addEventListener("click", event => {
      const link = event.target.closest("[data-section], [data-page]");
      if (!link) return;

      const sectionId = link.dataset.section || link.dataset.page;
      const target = sectionId && document.getElementById(sectionId);
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
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* -------------------------
     City modal and styles
  ------------------------- */

  function createCityModal() {
    if (document.getElementById("taqvoCityModal")) return;

    const modal = document.createElement("div");
    modal.id = "taqvoCityModal";
    modal.innerHTML = `
      <div class="taqvo-city-backdrop"></div>
      <div class="taqvo-city-dialog" role="dialog" aria-modal="true">
        <div class="taqvo-city-header">
          <strong>${escapeHTML(t("selectCity"))}</strong>
          <button type="button" id="taqvoCityClose" aria-label="${escapeHTML(t("close"))}">✕</button>
        </div>
        <input id="taqvoCitySearch" type="search"
          placeholder="${escapeHTML(t("searchCity"))}" autocomplete="off" />
        <div id="taqvoCityResults" aria-live="polite">
          <div class="taqvo-city-empty">${escapeHTML(t("searchCity"))}</div>
        </div>
      </div>`;
    document.body.appendChild(modal);

    if (!document.getElementById("taqvoCityModalStyles")) {
      const style = document.createElement("style");
      style.id = "taqvoCityModalStyles";
      style.textContent = `
        #taqvoCityModal{display:none;position:fixed;inset:0;z-index:99999;font-family:inherit}
        #taqvoCityModal.open{display:block}
        .taqvo-city-backdrop{position:absolute;inset:0;background:rgba(0,0,0,.78);backdrop-filter:blur(7px)}
        .taqvo-city-dialog{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
          width:calc(100% - 32px);max-width:420px;max-height:80vh;overflow:hidden;box-sizing:border-box;
          padding:20px;border:1px solid rgba(255,190,65,.35);border-radius:20px;background:#101014;color:#fff;
          box-shadow:0 15px 60px rgba(0,0,0,.5)}
        .taqvo-city-header{display:flex;justify-content:space-between;align-items:center;gap:12px;
          margin-bottom:16px;color:#ffd36a}
        #taqvoCityClose{border:0;background:transparent;color:#fff;font-size:22px;padding:4px 8px;cursor:pointer}
        #taqvoCitySearch{width:100%;box-sizing:border-box;padding:14px;border-radius:12px;
          border:1px solid #454047;outline:none;background:#1b1a20;color:#fff;font-size:16px}
        #taqvoCityResults{overflow-y:auto;max-height:50vh;margin-top:12px}
        .taqvo-city-result{width:100%;display:block;padding:13px 12px;margin:5px 0;border:1px solid #302d31;
          border-radius:10px;background:#19181d;color:#fff;text-align:left;font-size:15px;cursor:pointer}
        .taqvo-city-result:active{background:#493719}
        .taqvo-city-empty{padding:16px 5px;color:#aaa;text-align:center}
        #taqvoToast{position:fixed;z-index:100000;bottom:28px;left:50%;transform:translate(-50%,20px);
          opacity:0;pointer-events:none;padding:12px 18px;border-radius:12px;background:#242126;color:#fff;
          border:1px solid rgba(255,190,65,.4);transition:.2s ease;max-width:85%;text-align:center}
        #taqvoToast.show{opacity:1;transform:translate(-50%,0)}
      `;
      document.head.appendChild(style);
    }

    document.getElementById("taqvoCityClose").addEventListener("click", closeCityModal);
    modal.querySelector(".taqvo-city-backdrop").addEventListener("click", closeCityModal);
    document.getElementById("taqvoCitySearch").addEventListener("input", handleCitySearch);
    document.addEventListener("keydown", event => {
      if (event.key === "Escape") closeCityModal();
    });
  }

  function openCityModal() {
    createCityModal();
    const modal = document.getElementById("taqvoCityModal");
    const input = document.getElementById("taqvoCitySearch");
    modal.classList.add("open");
    input.value = "";
    document.getElementById("taqvoCityResults").innerHTML =
      `<div class="taqvo-city-empty">${escapeHTML(t("searchCity"))}</div>`;
    input.focus();
  }

  function closeCityModal() {
    document.getElementById("taqvoCityModal")?.classList.remove("open");
  }

  /* -------------------------
     City search
  ------------------------- */

  function handleCitySearch(event) {
    const query = event.target.value.trim();
    clearTimeout(searchTimer);
    citySearchRequest += 1;

    if (query.length < 2) {
      document.getElementById("taqvoCityResults").innerHTML =
        `<div class="taqvo-city-empty">${escapeHTML(t("searchCity"))}</div>`;
      return;
    }
    searchTimer = setTimeout(() => searchCities(query), CONFIG.SEARCH_DELAY);
  }

  async function searchCities(query) {
    const results = document.getElementById("taqvoCityResults");
    if (!results) return;
    const requestId = ++citySearchRequest;
    setLoading(results);

    try {
      const params = new URLSearchParams({ q: query, count: "15", language });
      const data = await apiRequest(`/api/prayer/cities?${params.toString()}`);
      if (requestId !== citySearchRequest) return;

      const cities = Array.isArray(data)
        ? data
        : data?.cities || data?.results || data?.data || [];

      if (!Array.isArray(cities) || cities.length === 0) {
        results.innerHTML = `<div class="taqvo-city-empty">${escapeHTML(t("cityNotFound"))}</div>`;
        return;
      }

      results.innerHTML = "";
      cities.forEach(city => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "taqvo-city-result";
        const name = city.name || city.city || city.display_name || city.name_ru || "Unknown";
        const country = city.country || city.country_name || "";
        button.textContent = country ? `${name}, ${country}` : name;
        button.addEventListener("click", () => selectCity(city));
        results.appendChild(button);
      });
    } catch (error) {
      console.error("City search error:", error);
      if (requestId !== citySearchRequest) return;
      results.innerHTML = `<div class="taqvo-city-empty">${escapeHTML(t("connectionError"))}</div>`;
    }
  }

  function normalizeCity(city) {
    return {
      name: city.name || city.city || city.display_name || "Unknown",
      country: city.country || city.country_name || "",
      latitude: Number(city.latitude ?? city.lat ?? city.location?.latitude),
      longitude: Number(city.longitude ?? city.lon ?? city.lng ?? city.location?.longitude),
      timezone: city.timezone || city.time_zone || CONFIG.DEFAULT_TIMEZONE
    };
  }

  async function selectCity(rawCity) {
    const city = normalizeCity(rawCity);
    if (!validCity(city)) {
      showToast(t("connectionError"));
      console.error("Invalid city coordinates:", rawCity);
      return false;
    }

    // Cancel any in-flight prayer request before switching city.
    prayerRequestId += 1;
    selectedCity = city;
    prayerData = null;
    lastCountdownValue = "";
    prayerSettings.timezone = city.timezone;
    prayerSettings.madhhab = "hanafi";

    saveJSON(STORAGE.city, selectedCity);
    savePrayerSettings();
    closeCityModal();
    updateCityName();
    updateCityDates();

    restorePrayerCache();
    await loadPrayerTimes();
    return true;
  }

  function updateCityName() {
    const name = selectedCity
      ? [selectedCity.name, selectedCity.country].filter(Boolean).join(", ")
      : t("chooseCity");

    ["#userLocation", "#selectedCity", "[data-selected-city]"].forEach(selector => {
      document.querySelectorAll(selector).forEach(element => {
        element.textContent = name;
      });
    });
  }

  /* -------------------------
     Prayer settings (Hanafi fixed)
  ------------------------- */

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
        : language === "uz-Cyrl"
          ? "Ҳисоблаш усули рақамини киритинг (стандарт 3):"
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
    savePrayerSettings();
    prayerData = null;
    loadPrayerTimes();
  }

  /* -------------------------
     Load prayer times safely
  ------------------------- */

  async function loadPrayerTimes() {
    if (!selectedCity) {
      updateCityName();
      return false;
    }
    if (!validCity(selectedCity)) {
      showToast(t("connectionError"));
      console.error("Saved city coordinates are invalid:", selectedCity);
      return false;
    }

    const requestId = ++prayerRequestId;
    const cacheAvailable = restorePrayerCache();

    const params = new URLSearchParams({
      latitude: String(selectedCity.latitude),
      longitude: String(selectedCity.longitude),
      timezone: getTimezone(),
      method: String(getPrayerSettings().method),
      madhhab: "hanafi"
    });

    try {
      const data = await apiRequest(`/api/prayer/today?${params.toString()}`);
      if (requestId !== prayerRequestId) return false;

      if (data?.success === false) throw new Error(data.message || "Prayer API error");

      const timings = data?.timings || data?.data?.timings;
      if (!timings || typeof timings !== "object") {
        throw new Error("Prayer API response has no timings object");
      }

      prayerData = {
        ...data,
        timings,
        hijri: data.hijri || data.data?.hijri || null,
        cached: false
      };

      savePrayerCache(prayerData);
      lastPrayerDateKey = getCityDateKey();
      renderPrayerTimes();
      renderPrayerNames();
      updateCityDates();
      updateNextPrayer();

      document.dispatchEvent(new CustomEvent("taqvo:prayer-loaded", {
        detail: prayerData
      }));
      return true;
    } catch (error) {
      if (requestId !== prayerRequestId) return false;
      console.error("Prayer loading error:", error);

      if (cacheAvailable || restorePrayerCache()) {
        showToast(t("offlineCache"));
      } else {
        showToast(t("connectionError"));
      }
      return false;
    }
  }

  /* -------------------------
     Render prayer times and names
  ------------------------- */

  function normalizePrayerTime(value) {
    if (!value) return "--:--";
    const match = String(value).match(/(\d{1,2}):(\d{2})/);
    if (!match) return "--:--";
    return `${pad(Number(match[1]))}:${match[2]}`;
  }

  function renderPrayerTimes() {
    if (!prayerData?.timings) return;

    PRAYERS.forEach(prayer => {
      const time = normalizePrayerTime(prayerData.timings[prayer.key]);
      const card = document.querySelector(`.prayer-item[data-prayer="${prayer.id}"]`);
      if (!card) return;

      const timeElement = card.querySelector(".prayer-time") ||
        card.querySelector("[data-prayer-time]") ||
        card.querySelector(".time");

      if (timeElement) {
        timeElement.textContent = time;
      } else {
        const fallback = card.querySelector("span:last-child");
        if (fallback) fallback.textContent = time;
      }
      card.dataset.time = time;
    });
  }

  function renderPrayerNames() {
    PRAYERS.forEach(prayer => {
      const card = document.querySelector(`.prayer-item[data-prayer="${prayer.id}"]`);
      if (!card) return;

      const nameElement = card.querySelector(".prayer-name") ||
        card.querySelector("[data-prayer-name]");

      if (nameElement) nameElement.textContent = prayer.names[language] || prayer.names.uz;
    });
  }

  /* -------------------------
     Next prayer countdown
  ------------------------- */

  function parsePrayerDate(time, baseDate) {
    const normalized = normalizePrayerTime(time);
    if (normalized === "--:--") return null;
    const [hours, minutes] = normalized.split(":").map(Number);
    const result = new Date(baseDate);
    result.setHours(hours, minutes, 0, 0);
    return result;
  }

  function updateNextPrayer() {
    if (!prayerData?.timings) return;

    const now = getCityDate();
    const schedule = PRAYERS.map(prayer => ({
      ...prayer,
      time: normalizePrayerTime(prayerData.timings[prayer.key])
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
      const firstPrayer = schedule[0];
      const date = parsePrayerDate(firstPrayer.time, tomorrow);
      if (date) next = { ...firstPrayer, date };
    }

    document.querySelectorAll(".prayer-item").forEach(card => {
      card.classList.remove("active", "next-prayer");
    });

    if (!next) return;

    const activeCard = document.querySelector(`.prayer-item[data-prayer="${next.id}"]`);
    activeCard?.classList.add("active", "next-prayer");

    const nameElement = document.getElementById("nextPrayerName");
    const countdownElement = document.getElementById("nextPrayerCountdown");

    if (nameElement) nameElement.textContent = next.names[language] || next.names.uz;

    if (countdownElement) {
      const secondsLeft = Math.max(0, Math.floor((next.date - now) / 1000));
      const hours = Math.floor(secondsLeft / 3600);
      const minutes = Math.floor((secondsLeft % 3600) / 60);
      const seconds = secondsLeft % 60;
      const value = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;

      if (value !== lastCountdownValue) {
        countdownElement.textContent = value;
        lastCountdownValue = value;
      }
    }
  }

  /* -------------------------
     Bind city/prayer UI events
  ------------------------- */

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

      const settingsButton = event.target.closest('[data-action="prayer-settings"]');
      if (settingsButton) {
        event.preventDefault();
        openPrayerSettings();
      }
    });

    updateCityName();

    if (selectedCity) {
      restorePrayerCache(); // instant display from this device
      loadPrayerTimes();    // refresh from server in background
    }

    if (!countdownTimer) {
      countdownTimer = setInterval(() => {
        updateNextPrayer();
        updateCityDates();

        // At city-local midnight, today's cache key changes; fetch new timings once.
        const todayKey = getCityDateKey();
        if (selectedCity && todayKey !== lastPrayerDateKey) {
          lastPrayerDateKey = todayKey;
          loadPrayerTimes();
        }
      }, 1000);
    }
  }

  /* -------------------------
     Public app API
  ------------------------- */

  window.TAQVO = {
    version: "2.1.0",
    get language() { return language; },
    get city() { return selectedCity; },
    get prayerData() { return prayerData; },
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
    setCity(city) { return selectCity(city); },
    refreshPrayerTimes() { return loadPrayerTimes(); }
  };

  /* -------------------------
     Start application
  ------------------------- */

  function init() {
    initTelegram();
    initLanguage();
    initNavigation();
    initCityAndPrayer();

    document.dispatchEvent(new CustomEvent("taqvo:ready"));

    console.log(
      "%c TAQVO PRO MAX ",
      "background:#111;color:#ffd700;font-weight:bold;padding:8px;"
    );
    console.log("TAQVO application initialized.");
    console.log("Prayer calculation: Hanafi (fixed; no madhhab selector).");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
