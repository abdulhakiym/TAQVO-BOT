"use strict";

/* =====================================================
   TAQVO PRO MAX — WORLDWIDE PRAYER TIMES
   Backend: https://taqvo-api-uz.onrender.com
===================================================== */

(() => {
    const API_BASE = "https://taqvo-api-uz.onrender.com";
    const CITY_STORAGE = "taqvo_selected_city";
    const SETTINGS_STORAGE = "taqvo_prayer_settings";

    const DEFAULT_SETTINGS = {
        method: 3,
        school: 1
    };

    const TEXT = {
        uz: {
            searchTitle: "Shaharni tanlang",
            searchPlaceholder: "Shahar nomini yozing...",
            searching: "Qidirilmoqda...",
            noResults: "Shahar topilmadi. Boshqa nom bilan urinib ko‘ring.",
            searchError: "Shaharlarni qidirishda xatolik. Qayta urinib ko‘ring.",
            choose: "Tanlash",
            settings: "Namoz sozlamalari",
            method: "Hisoblash usuli",
            school: "Asr mazhabi",
            hanafi: "Hanafiy",
            other: "Shofi’iy / Molikiy / Hanbaliy",
            save: "Saqlash",
            cancel: "Bekor qilish",
            loading: "Namoz vaqtlari yuklanmoqda...",
            prayerError: "Namoz vaqtlarini olib bo‘lmadi. Qayta urinib ko‘ring.",
            next: "Keyingi namoz",
            today: "Bugungi namoz vaqtlari",
            methods: [
                "Muslim World League",
                "Islamic Society of North America",
                "Egyptian General Authority",
                "Umm al-Qura University, Makkah",
                "University of Islamic Sciences, Karachi",
                "Institute of Geophysics, Tehran",
                "Gulf Region",
                "Kuwait",
                "Qatar",
                "Majlis Ugama Islam Singapura",
                "Union Organization Islamic de France",
                "Diyanet İşleri Başkanlığı, Turkey",
                "Spiritual Administration of Muslims of Russia"
            ]
        },
        "uz-Cyrl": {
            searchTitle: "Шаҳарни танланг",
            searchPlaceholder: "Шаҳар номини ёзинг...",
            searching: "Қидирилмоқда...",
            noResults: "Шаҳар топилмади. Бошқа ном билан уриниб кўринг.",
            searchError: "Шаҳарларни қидиришда хатолик. Қайта уриниб кўринг.",
            choose: "Танлаш",
            settings: "Намоз созламалари",
            method: "Ҳисоблаш усули",
            school: "Аср мазҳаби",
            hanafi: "Ҳанафий",
            other: "Шофеъий / Моликий / Ҳанбалий",
            save: "Сақлаш",
            cancel: "Бекор қилиш",
            loading: "Намоз вақтлари юкланмоқда...",
            prayerError: "Намоз вақтларини олиб бўлмади. Қайта уриниб кўринг.",
            next: "Кейинги намоз",
            today: "Бугунги намоз вақтлари",
            methods: [
                "Muslim World League",
                "Islamic Society of North America",
                "Egyptian General Authority",
                "Umm al-Qura University, Makkah",
                "University of Islamic Sciences, Karachi",
                "Institute of Geophysics, Tehran",
                "Gulf Region",
                "Kuwait",
                "Qatar",
                "Majlis Ugama Islam Singapura",
                "Union Organization Islamic de France",
                "Diyanet İşleri Başkanlığı, Turkey",
                "Spiritual Administration of Muslims of Russia"
            ]
        },
        ru: {
            searchTitle: "Выберите город",
            searchPlaceholder: "Введите название города...",
            searching: "Поиск...",
            noResults: "Город не найден. Попробуйте другое название.",
            searchError: "Ошибка поиска городов. Попробуйте ещё раз.",
            choose: "Выбрать",
            settings: "Настройки намаза",
            method: "Метод расчёта",
            school: "Мазхаб для Асра",
            hanafi: "Ханафитский",
            other: "Шафиитский / Маликитский / Ханбалитский",
            save: "Сохранить",
            cancel: "Отмена",
            loading: "Загрузка времени намаза...",
            prayerError: "Не удалось получить время намаза. Попробуйте ещё раз.",
            next: "Следующий намаз",
            today: "Время намаза на сегодня",
            methods: [
                "Muslim World League",
                "Islamic Society of North America",
                "Egyptian General Authority",
                "Umm al-Qura University, Makkah",
                "University of Islamic Sciences, Karachi",
                "Institute of Geophysics, Tehran",
                "Gulf Region",
                "Kuwait",
                "Qatar",
                "Majlis Ugama Islam Singapura",
                "Union Organization Islamic de France",
                "Diyanet İşleri Başkanlığı, Turkey",
                "Spiritual Administration of Muslims of Russia"
            ]
        }
    };

    const PRAYER_KEYS = ["fajr", "dhuhr", "asr", "maghrib", "isha"];

    const PRAYER_NAMES = {
        uz: ["Bomdod", "Peshin", "Asr", "Shom", "Xufton"],
        "uz-Cyrl": ["Бомдод", "Пешин", "Аср", "Шом", "Хуфтон"],
        ru: ["Фаджр", "Зухр", "Аср", "Магриб", "Иша"]
    };

    let selectedCity = null;
    let prayerSettings = { ...DEFAULT_SETTINGS };
    let prayerData = null;
    let countdownTimer = null;
    let searchTimer = null;
    let searchController = null;
    let currentLanguage = "uz";

    function language() {
        const value = document.getElementById("languageSelect")?.value;
        return TEXT[value] ? value : currentLanguage;
    }

    function t(key) {
        return TEXT[language()][key] ?? TEXT.uz[key] ?? key;
    }

    function escapeHTML(value) {
        return String(value ?? "").replace(/[&<>"']/g, character => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        })[character]);
    }

    function readStorage() {
        try {
            const city = localStorage.getItem(CITY_STORAGE);
            const settings = localStorage.getItem(SETTINGS_STORAGE);

            if (city) selectedCity = JSON.parse(city);

            if (settings) {
                const parsed = JSON.parse(settings);
                prayerSettings = {
                    method: Number(parsed.method ?? DEFAULT_SETTINGS.method),
                    school: Number(parsed.school ?? DEFAULT_SETTINGS.school)
                };
            }
        } catch (error) {
            console.warn("TAQVO prayer settings could not be loaded.");
        }
    }

    function saveCity(city) {
        selectedCity = city;

        try {
            localStorage.setItem(CITY_STORAGE, JSON.stringify(city));
        } catch (error) {
            console.warn("Selected city could not be saved.");
        }

        updateLocationLabel();
        closeModal();
        loadPrayerTimes();
    }

    function updateLocationLabel() {
        const element = document.getElementById("userLocation");

        if (!element || !selectedCity) return;

        element.textContent = [
            selectedCity.name,
            selectedCity.country
        ].filter(Boolean).join(", ");
    }

    function showToast(message) {
        let toast = document.getElementById("taqvoToast");

        if (!toast) {
            toast = document.createElement("div");
            toast.id = "taqvoToast";

            Object.assign(toast.style, {
                position: "fixed",
                zIndex: "10010",
                left: "50%",
                bottom: "100px",
                transform: "translateX(-50%)",
                width: "calc(100% - 40px)",
                maxWidth: "400px",
                padding: "13px 16px",
                border: "1px solid rgba(255,215,0,.3)",
                borderRadius: "13px",
                background: "#17151A",
                color: "#FFD700",
                textAlign: "center",
                fontSize: "13px"
            });

            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.hidden = false;

        clearTimeout(showToast.timer);
        showToast.timer = setTimeout(() => {
            toast.hidden = true;
        }, 3000);
    }

    function createModal() {
        let modal = document.getElementById("prayerModal");

        if (modal) return modal;

        modal = document.createElement("div");
        modal.id = "prayerModal";

        Object.assign(modal.style, {
            position: "fixed",
            inset: "0",
            zIndex: "10000",
            display: "none",
            alignItems: "center",
            justifyContent: "center",
            padding: "18px",
            background: "rgba(0,0,0,.78)",
            backdropFilter: "blur(8px)"
        });

        modal.innerHTML = `
            <section style="
                width:100%;
                max-width:420px;
                max-height:85vh;
                overflow:auto;
                padding:22px;
                border:1px solid rgba(255,215,0,.3);
                border-radius:20px;
                background:#111015;
                color:#fff;
                box-shadow:0 15px 50px rgba(0,0,0,.5);
            ">
                <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
                    <h2 id="prayerModalTitle" style="font-size:20px;margin:0"></h2>
                    <button type="button" data-prayer-close style="
                        border:0;background:transparent;color:#FFD700;
                        font-size:25px;padding:4px 8px
                    " aria-label="Close">×</button>
                </div>
                <div id="prayerModalBody" style="margin-top:18px"></div>
            </section>
        `;

        document.body.appendChild(modal);

        modal.addEventListener("click", event => {
            if (event.target === modal ||
                event.target.closest("[data-prayer-close]")) {
                closeModal();
            }
        });

        return modal;
    }

    function openModal(title, content) {
        const modal = createModal();

        document.getElementById("prayerModalTitle").textContent = title;
        document.getElementById("prayerModalBody").innerHTML = content;

        modal.style.display = "flex";
        document.body.style.overflow = "hidden";
    }

    function closeModal() {
        const modal = document.getElementById("prayerModal");

        if (modal) modal.style.display = "none";

        document.body.style.overflow = "";
    }

    function openCitySearch() {
        openModal(t("searchTitle"), `
            <input
                id="citySearchInput"
                type="search"
                autocomplete="off"
                placeholder="${escapeHTML(t("searchPlaceholder"))}"
                style="
                    width:100%;box-sizing:border-box;padding:14px;
                    border:1px solid rgba(255,215,0,.35);
                    border-radius:12px;background:#08080b;
                    color:#fff;font-size:16px;outline:none
                "
            >
            <p id="citySearchStatus" style="color:#aaa;font-size:13px"></p>
            <div id="citySearchResults"></div>
        `);

        const input = document.getElementById("citySearchInput");
        input?.focus();

        input?.addEventListener("input", () => {
            clearTimeout(searchTimer);

            const query = input.value.trim();

            if (query.length < 2) {
                document.getElementById("citySearchStatus").textContent = "";
                document.getElementById("citySearchResults").innerHTML = "";
                return;
            }

            searchTimer = setTimeout(() => searchCities(query), 400);
        });

        if (selectedCity) {
            document.getElementById("citySearchStatus").textContent =
                `${selectedCity.name}, ${selectedCity.country}`;
        }
    }

    async function searchCities(query) {
        const status = document.getElementById("citySearchStatus");
        const resultsBox = document.getElementById("citySearchResults");

        if (!status || !resultsBox) return;

        if (searchController) searchController.abort();
        searchController = new AbortController();

        status.textContent = t("searching");
        resultsBox.innerHTML = "";

        try {
            const lang = language() === "ru" ? "ru" : "en";

            const url = new URL(`${API_BASE}/api/prayer/cities`);
            url.searchParams.set("q", query);
            url.searchParams.set("count", "10");
            url.searchParams.set("language", lang);

            const response = await fetch(url, {
                method: "GET",
                signal: searchController.signal
            });

            if (!response.ok) throw new Error("City search failed");

            const data = await response.json();

            if (!data.success || !data.results?.length) {
                status.textContent = t("noResults");
                return;
            }

            status.textContent = "";

            resultsBox.innerHTML = data.results.map((city, index) => `
                <button
                    type="button"
                    data-city-index="${index}"
                    style="
                        display:block;width:100%;text-align:left;
                        padding:14px 10px;margin-top:7px;
                        border:1px solid rgba(255,215,0,.15);
                        border-radius:12px;background:#1b1920;color:#fff;
                    "
                >
                    <strong>${escapeHTML(city.name)}</strong>
                    <span style="display:block;color:#aaa;font-size:12px;margin-top:4px">
                        ${escapeHTML([city.region, city.country].filter(Boolean).join(", "))}
                    </span>
                </button>
            `).join("");

            resultsBox.querySelectorAll("[data-city-index]").forEach(button => {
                button.addEventListener("click", () => {
                    const city = data.results[Number(button.dataset.cityIndex)];

                    saveCity({
                        id: city.id,
                        name: city.name,
                        country: city.country,
                        region: city.region,
                        latitude: city.latitude,
                        longitude: city.longitude,
                        timezone: city.timezone
                    });
                });
            });

        } catch (error) {
            if (error.name === "AbortError") return;

            console.error("TAQVO city search error:", error);
            status.textContent = t("searchError");
        }
    }

    function openPrayerSettings() {
        const methods = t("methods");
        const methodOptions = methods.map((name, index) => `
            <option value="${index}" ${prayerSettings.method === index ? "selected" : ""}>
                ${escapeHTML(name)}
            </option>
        `).join("");

        openModal(t("settings"), `
            <label style="display:block;margin-bottom:8px">${escapeHTML(t("method"))}</label>
            <select id="prayerMethod" style="
                width:100%;padding:13px;margin-bottom:20px;
                border-radius:10px;background:#08080b;color:#fff;
                border:1px solid rgba(255,215,0,.3)
            ">
                ${methodOptions}
            </select>

            <label style="display:block;margin-bottom:8px">${escapeHTML(t("school"))}</label>
            <select id="prayerSchool" style="
                width:100%;padding:13px;border-radius:10px;
                background:#08080b;color:#fff;
                border:1px solid rgba(255,215,0,.3)
            ">
                <option value="1" ${prayerSettings.school === 1 ? "selected" : ""}>
                    ${escapeHTML(t("hanafi"))}
                </option>
                <option value="0" ${prayerSettings.school === 0 ? "selected" : ""}>
                    ${escapeHTML(t("other"))}
                </option>
            </select>

            <div style="display:flex;gap:10px;margin-top:22px">
                <button type="button" id="savePrayerSettings" style="
                    flex:1;padding:13px;border:0;border-radius:10px;
                    background:linear-gradient(90deg,#FF8C00,#FFD700);
                    color:#111;font-weight:700
                ">${escapeHTML(t("save"))}</button>
                <button type="button" data-prayer-close style="
                    padding:13px 16px;border:1px solid #555;
                    border-radius:10px;background:#222;color:#fff
                ">${escapeHTML(t("cancel"))}</button>
            </div>
        `);

        document.getElementById("savePrayerSettings")
            ?.addEventListener("click", () => {
                prayerSettings = {
                    method: Number(document.getElementById("prayerMethod").value),
                    school: Number(document.getElementById("prayerSchool").value)
                };

                try {
                    localStorage.setItem(
                        SETTINGS_STORAGE,
                        JSON.stringify(prayerSettings)
                    );
                } catch (error) {
                    console.warn("Prayer settings could not be saved.");
                }

                closeModal();

                if (selectedCity) loadPrayerTimes();
            });
    }

    async function loadPrayerTimes() {
        if (!selectedCity) return;

        showToast(t("loading"));

        const params = new URLSearchParams({
            latitude: String(selectedCity.latitude),
            longitude: String(selectedCity.longitude),
            timezone: selectedCity.timezone,
            method: String(prayerSettings.method),
            school: String(prayerSettings.school)
        });

        try {
            const response = await fetch(
                `${API_BASE}/api/prayer/today?${params.toString()}`
            );

            if (!response.ok) throw new Error("Prayer times request failed");

            const data = await response.json();

            if (!data.success || !data.timings) {
                throw new Error("Invalid prayer times response");
            }

            prayerData = data;
            renderPrayerTimes();
            updateHijriDate();
            startCountdown();

        } catch (error) {
            console.error("TAQVO prayer times error:", error);
            showToast(t("prayerError"));
        }
    }

    function renderPrayerTimes() {
        if (!prayerData) return;

        PRAYER_KEYS.forEach((key, index) => {
            const item = document.querySelector(`[data-prayer="${key}"]`);

            if (!item) return;

            const time = item.querySelector("strong");

            if (time) {
                time.textContent = prayerData.timings[key] || "--:--";
            }
        });

        updateLocationLabel();
    }

    function updateHijriDate() {
        const hijriElement = document.getElementById("hijriDate");
        const gregorianElement = document.getElementById("gregorianDate");

        const hijri = prayerData?.hijri;

        if (hijriElement && hijri?.date) {
            const day = hijri.day || "";
            const month = hijri.month?.en || "";
            const year = hijri.year || "";

            hijriElement.textContent = [day, month, year]
                .filter(Boolean).join(" ");
        }

        if (gregorianElement && prayerData?.date) {
            const date = new Date(`${prayerData.date}T12:00:00`);

            gregorianElement.textContent = new Intl.DateTimeFormat(
                language() === "ru" ? "ru-RU" :
                language() === "uz-Cyrl" ? "uz-Cyrl-UZ" : "uz-UZ",
                { day: "numeric", month: "long", year: "numeric" }
            ).format(date);
        }
    }

    function startCountdown() {
        clearInterval(countdownTimer);
        updateCountdown();
        countdownTimer = setInterval(updateCountdown, 1000);
    }

    function updateCountdown() {
        if (!selectedCity || !prayerData) return;

        const now = new Date();

        const localNow = new Date(
            now.toLocaleString("en-US", { timeZone: selectedCity.timezone })
        );

        const currentMinutes = localNow.getHours() * 60 + localNow.getMinutes();
        const currentSeconds = localNow.getSeconds();

        const prayerTimes = PRAYER_KEYS.map((key, index) => {
            const value = prayerData.timings[key];
            const [hours, minutes] = value.split(":").map(Number);

            return {
                key,
                name: PRAYER_NAMES[language()][index],
                minutes: hours * 60 + minutes
            };
        });

        let nextPrayer = prayerTimes.find(
            prayer => prayer.minutes > currentMinutes
        );

        let targetDate = new Date(localNow);

        if (!nextPrayer) {
            nextPrayer = prayerTimes[0];
            targetDate.setDate(targetDate.getDate() + 1);
        }

        const difference = (
            (targetDate.getDate() !== localNow.getDate()
                ? 24 * 60
                : 0) +
            nextPrayer.minutes -
            currentMinutes
        ) * 60 - currentSeconds;

        const safeDifference = Math.max(0, difference);

        const hours = Math.floor(safeDifference / 3600);
        const minutes = Math.floor((safeDifference % 3600) / 60);
        const seconds = safeDifference % 60;

        const nameElement = document.getElementById("nextPrayerName");
        const countdownElement = document.getElementById("nextPrayerCountdown");

        if (nameElement) nameElement.textContent = nextPrayer.name;

        if (countdownElement) {
            countdownElement.textContent = [
                String(hours).padStart(2, "0"),
                String(minutes).padStart(2, "0"),
                String(seconds).padStart(2, "0")
            ].join(":");
        }

        document.querySelectorAll(".prayer-item").forEach(item => {
            item.classList.toggle(
                "active",
                item.dataset.prayer === nextPrayer.key
            );
        });
    }

    function interceptActions() {
        document.addEventListener("click", event => {
            const target = event.target;

            if (!(target instanceof Element)) return;

            const button = target.closest("[data-action]");
            if (!button) return;

            const action = button.dataset.action;

            if (action === "select-city") {
                event.preventDefault();
                event.stopImmediatePropagation();
                openCitySearch();
            }

            if (action === "prayer-settings") {
                event.preventDefault();
                event.stopImmediatePropagation();
                openPrayerSettings();
            }
        }, true);
    }

    function init() {
        readStorage();
        interceptActions();

        if (selectedCity) {
            updateLocationLabel();
            loadPrayerTimes();
        }

        document.getElementById("languageSelect")
            ?.addEventListener("change", () => {
                currentLanguage = language();

                if (prayerData) {
                    renderPrayerTimes();
                    updateHijriDate();
                    updateCountdown();
                }
            });

        console.info("TAQVO prayer module initialized.");
    }

    document.addEventListener("DOMContentLoaded", init);
})();
