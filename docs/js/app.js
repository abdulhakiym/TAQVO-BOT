"use strict";

/* =====================================================
   TAQVO PRO MAX — APPLICATION CORE
   Version 1.2
   Languages: Uzbek Latin, Uzbek Cyrillic, Russian
===================================================== */

const TAQVO = (() => {
    const STORAGE_KEY = "taqvo_language";
    const supportedLanguages = ["uz", "uz-Cyrl", "ru"];

    const translations = {
        uz: {
            brandSubtitle: "Qalbga nur, hayotga hidoyat",
            locationLabel: "SIZNING MANZILINGIZ",
            selectCity: "Shaharni tanlang",
            hijriLabel: "Hijriy sana",
            gregorianLabel: "Milodiy sana",
            prayerLabel: "IBODAT VAQTLARI",
            prayerTitle: "Namoz vaqtlari",
            prayerSettings: "Sozlash ⚙",
            fajr: "Bomdod", dhuhr: "Peshin", asr: "Asr",
            maghrib: "Shom", isha: "Xufton",
            nextPrayer: "KEYINGI NAMOZ",
            personalLabel: "SIZNING IBODATINGIZ",
            personalTitle: "Shaxsiy kabinet",
            myQuran: "Qur'onim",
            lastReading: "Oxirgi o‘qilgan joy",
            myKhatm: "Xatmim",
            khatmProgress: "Xatm jarayoni",
            myTasbeeh: "Tasbehim",
            todayZikr: "Bugungi zikrlar",
            myRanking: "Reytingim",
            myPosition: "Mening o‘rnim",
            saved: "Saqlanganlarim",
            savedContent: "Oyat, hadis va duolar",
            myMuhasaba: "Muhosabam",
            dailyActions: "Kunlik amallar",
            myGoals: "Maqsadlarim",
            hifzGoals: "Hifz va ibodat rejalari",
            myReminders: "Eslatmalarim",
            personalNotifications: "Shaxsiy bildirishnomalar",
            dailyLabel: "HAR KUNGI MA'NAVIY OZUQA",
            dailyTitle: "Bugungi eslatma",
            ayahOfDay: "KUN OYATI",
            dailyAyahMeaning: "Bas, Meni eslanglar, Men ham sizlarni eslayman.",
            ayahSource: "Al-Baqara, 152-oyat",
            readMore: "Batafsil o‘qish",
            continueLabel: "DAVOM ETING",
            continueQuran: "Qur'on tilovatini davom ettiring",
            continueDescription: "Oxirgi o‘qigan sahifangizga qayting.",
            mainLabel: "BARCHA XIZMATLAR",
            mainTitle: "Asosiy bo‘limlar",
            quranFeatureLabel: "01 · QUR'ONI KARIM",
            quranTitle: "Qur'oni Karim",
            quranDescription: "114 sura · 30 juz · 604 sahifa",
            openQuran: "Mushafni ochish →",
            prayerQibla: "Namoz vaqtlari + Qibla",
            tasbeeh: "Elektron tasbeh",
            adhkar: "Tonggi va kechki zikrlar",
            duas: "Duo va munojotlar",
            hadith: "Sahih hadislar",
            quizTitle: "TAQVO QUIZ",
            aiTitle: "TAQVO AI",
            ibadah: "Ibodat qo‘llanmasi",
            seerah: "Siyrat va sahobalar",
            fiqh: "Fiqh va to‘rt mazhab",
            names: "Allohning 99 go‘zal ismi",
            hajjUmrah: "Haj, Umra va ziyorat",
            muhasaba: "Kunlik muhosaba",
            tajweed: "Qur'on ta'limi va tajvid",
            media: "Islomiy media va kutubxona",
            extrasLabel: "QO‘SHIMCHA IMKONIYATLAR",
            extrasTitle: "TAQVO xizmatlari",
            taqvoDaily: "TAQVO DAILY",
            hifz: "HIFZ",
            hijriCalendar: "Hijriy taqvim",
            family: "Oila va farzandlar",
            muhasabaPlus: "MUHOSABA PLUS",
            taqvoAudio: "TAQVO AUDIO",
            arabic: "Arab tili",
            ilmMajlisi: "ILM MAJLISI",
            fasting: "Ro‘za taqvimi",
            dailyContent: "Kun oyati va hadisi",
            ziyarat: "Ziyorat yo‘riqnomasi",
            footerText: "Ilm, ibodat va go‘zal hayot sari.",
            home: "Bosh sahifa",
            quranNav: "Qur'on",
            tasbeehNav: "Tasbeh",
            profile: "Profil",
            notificationsLabel: "Bildirishnomalar",
            languageLabel: "Tilni tanlash",
            loading: "Yuklanmoqda...",
            soon: "Bu bo‘lim hali ishga tushirilmagan. Tez orada taqdim etiladi.",
            cityNotice: "Shahar tanlash xizmati backendga ulangandan keyin ishlaydi.",
            prayerNotice: "Namoz vaqtlarini olish xizmati hali ulanmagan.",
            notificationNotice: "Bildirishnomalar sozlamasi hali ulanmagan.",
            telegramNotice: "Bu xizmat Telegram Mini App ichida ishlashga mo‘ljallangan.",
            languageChanged: "Til o‘zgartirildi.",
            hijriUnavailable: "Hijriy sana aniqlanmadi"
        },

        "uz-Cyrl": {
            brandSubtitle: "Қалбга нур, ҳаётга ҳидоят",
            locationLabel: "СИЗНИНГ МАНЗИЛИНГИЗ",
            selectCity: "Шаҳарни танланг",
            hijriLabel: "Ҳижрий сана",
            gregorianLabel: "Милодий сана",
            prayerLabel: "ИБОДАТ ВАҚТЛАРИ",
            prayerTitle: "Намоз вақтлари",
            prayerSettings: "Созлаш ⚙",
            fajr: "Бомдод", dhuhr: "Пешин", asr: "Аср",
            maghrib: "Шом", isha: "Хуфтон",
            nextPrayer: "КЕЙИНГИ НАМОЗ",
            personalLabel: "СИЗНИНГ ИБОДАТИНГИЗ",
            personalTitle: "Шахсий кабинет",
            myQuran: "Қуръоним",
            lastReading: "Охирги ўқилган жой",
            myKhatm: "Хатмим",
            khatmProgress: "Хатм жараёни",
            myTasbeeh: "Тасбеҳим",
            todayZikr: "Бугунги зикрлар",
            myRanking: "Рейтингим",
            myPosition: "Менинг ўрним",
            saved: "Сақланганларим",
            savedContent: "Оят, ҳадис ва дуолар",
            myMuhasaba: "Муҳосабам",
            dailyActions: "Кунлик амаллар",
            myGoals: "Мақсадларим",
            hifzGoals: "Ҳифз ва ибодат режалари",
            myReminders: "Эслатмаларим",
            personalNotifications: "Шахсий билдиришномалар",
            dailyLabel: "ҲАР КУНГИ МАЪНАВИЙ ОЗУҚА",
            dailyTitle: "Бугунги эслатма",
            ayahOfDay: "КУН ОЯТИ",
            dailyAyahMeaning: "Бас, Мени эсланглар, Мен ҳам сизларни эслайман.",
            ayahSource: "Бақара сураси, 152-оят",
            readMore: "Батафсил ўқиш",
            continueLabel: "ДАВОМ ЭТИНГ",
            continueQuran: "Қуръон тиловатини давом эттиринг",
            continueDescription: "Охирги ўқиган саҳифангизга қайтинг.",
            mainLabel: "БАРЧА ХИЗМАТЛАР",
            mainTitle: "Асосий бўлимлар",
            quranFeatureLabel: "01 · ҚУРЪОНИ КАРИМ",
            quranTitle: "Қуръони Карим",
            quranDescription: "114 сура · 30 жуз · 604 саҳифа",
            openQuran: "Мусҳафни очиш →",
            prayerQibla: "Намоз вақтлари + Қибла",
            tasbeeh: "Электрон тасбеҳ",
            adhkar: "Тонгги ва кечки зикрлар",
            duas: "Дуо ва муножотлар",
            hadith: "Саҳиҳ ҳадислар",
            quizTitle: "TAQVO QUIZ",
            aiTitle: "TAQVO AI",
            ibadah: "Ибодат қўлланмаси",
            seerah: "Сийрат ва саҳобалар",
            fiqh: "Фиқҳ ва тўрт мазҳаб",
            names: "Аллоҳнинг 99 гўзал исми",
            hajjUmrah: "Ҳаж, Умра ва зиёрат",
            muhasaba: "Кунлик муҳосаба",
            tajweed: "Қуръон таълими ва тажвид",
            media: "Исломий медиа ва кутубхона",
            extrasLabel: "ҚЎШИМЧА ИМКОНИЯТЛАР",
            extrasTitle: "TAQVO хизматлари",
            taqvoDaily: "TAQVO DAILY",
            hifz: "ҲИФЗ",
            hijriCalendar: "Ҳижрий тақвим",
            family: "Оила ва фарзандлар",
            muhasabaPlus: "МУҲОСАБА PLUS",
            taqvoAudio: "TAQVO AUDIO",
            arabic: "Араб тили",
            ilmMajlisi: "ИЛМ МАЖЛИСИ",
            fasting: "Рўза тақвими",
            dailyContent: "Кун ояти ва ҳадиси",
            ziyarat: "Зиёрат йўриқномаси",
            footerText: "Илм, ибодат ва гўзал ҳаёт сари.",
            home: "Бош саҳифа",
            quranNav: "Қуръон",
            tasbeehNav: "Тасбеҳ",
            profile: "Профиль",
            notificationsLabel: "Билдиришномалар",
            languageLabel: "Тилни танлаш",
            loading: "Юкланмоқда...",
            soon: "Бу бўлим ҳали ишга туширилмаган. Тез орада тақдим этилади.",
            cityNotice: "Шаҳар танлаш хизмати backend'га улангандан кейин ишлайди.",
            prayerNotice: "Намоз вақтларини олиш хизмати ҳали уланмаган.",
            notificationNotice: "Билдиришномалар созламаси ҳали уланмаган.",
            telegramNotice: "Бу хизмат Telegram Mini App ичида ишлашга мўлжалланган.",
            languageChanged: "Тил ўзгартирилди.",
            hijriUnavailable: "Ҳижрий сана аниқланмади"
        },

        ru: {
            brandSubtitle: "Свет сердцу, руководство жизни",
            locationLabel: "ВАШЕ МЕСТОПОЛОЖЕНИЕ",
            selectCity: "Выберите город",
            hijriLabel: "Дата по хиджре",
            gregorianLabel: "Григорианская дата",
            prayerLabel: "ВРЕМЕНА ПОКЛОНЕНИЯ",
            prayerTitle: "Время намаза",
            prayerSettings: "Настройки ⚙",
            fajr: "Фаджр", dhuhr: "Зухр", asr: "Аср",
            maghrib: "Магриб", isha: "Иша",
            nextPrayer: "СЛЕДУЮЩИЙ НАМАЗ",
            personalLabel: "ВАШЕ ПОКЛОНЕНИЕ",
            personalTitle: "Личный кабинет",
            myQuran: "Мой Коран",
            lastReading: "Последнее чтение",
            myKhatm: "Мой хатм",
            khatmProgress: "Прогресс чтения",
            myTasbeeh: "Мой тасбих",
            todayZikr: "Зикры за сегодня",
            myRanking: "Мой рейтинг",
            myPosition: "Моя позиция",
            saved: "Сохранённое",
            savedContent: "Аяты, хадисы и дуа",
            myMuhasaba: "Мухасаба",
            dailyActions: "Ежедневные дела",
            myGoals: "Мои цели",
            hifzGoals: "Планы заучивания и поклонения",
            myReminders: "Мои напоминания",
            personalNotifications: "Личные уведомления",
            dailyLabel: "ДУХОВНАЯ ПИЩА НА КАЖДЫЙ ДЕНЬ",
            dailyTitle: "Напоминание дня",
            ayahOfDay: "АЯТ ДНЯ",
            dailyAyahMeaning: "Поминайте Меня, и Я буду помнить о вас.",
            ayahSource: "Сура «Аль-Бакара», аят 152",
            readMore: "Подробнее",
            continueLabel: "ПРОДОЛЖАЙТЕ",
            continueQuran: "Продолжите чтение Корана",
            continueDescription: "Вернитесь к последней прочитанной странице.",
            mainLabel: "ВСЕ СЕРВИСЫ",
            mainTitle: "Основные разделы",
            quranFeatureLabel: "01 · СВЯЩЕННЫЙ КОРАН",
            quranTitle: "Священный Коран",
            quranDescription: "114 сур · 30 джузов · 604 страницы",
            openQuran: "Открыть Мусхаф →",
            prayerQibla: "Время намаза + Кибла",
            tasbeeh: "Электронный тасбих",
            adhkar: "Утренние и вечерние зикры",
            duas: "Дуа и мольбы",
            hadith: "Достоверные хадисы",
            quizTitle: "TAQVO QUIZ",
            aiTitle: "TAQVO AI",
            ibadah: "Руководство по поклонению",
            seerah: "Сира и сподвижники",
            fiqh: "Фикх и четыре мазхаба",
            names: "99 прекрасных имён Аллаха",
            hajjUmrah: "Хадж, Умра и зиярат",
            muhasaba: "Ежедневная мухасаба",
            tajweed: "Обучение Корану и таджвид",
            media: "Исламские медиа и библиотека",
            extrasLabel: "ДОПОЛНИТЕЛЬНЫЕ ВОЗМОЖНОСТИ",
            extrasTitle: "Сервисы TAQVO",
            taqvoDaily: "TAQVO DAILY",
            hifz: "ХИФЗ",
            hijriCalendar: "Исламский календарь",
            family: "Семья и дети",
            muhasabaPlus: "МУХАСАБА PLUS",
            taqvoAudio: "TAQVO AUDIO",
            arabic: "Арабский язык",
            ilmMajlisi: "ИЛМ МАДЖЛИСИ",
            fasting: "Календарь поста",
            dailyContent: "Аят и хадис дня",
            ziyarat: "Путеводитель по зиярату",
            footerText: "На пути к знаниям, поклонению и благой жизни.",
            home: "Главная",
            quranNav: "Коран",
            tasbeehNav: "Тасбих",
            profile: "Профиль",
            notificationsLabel: "Уведомления",
            languageLabel: "Выбор языка",
            loading: "Загрузка...",
            soon: "Этот раздел ещё не запущен. Скоро он станет доступен.",
            cityNotice: "Выбор города станет доступен после подключения backend.",
            prayerNotice: "Сервис времени намаза ещё не подключён.",
            notificationNotice: "Настройки уведомлений ещё не подключены.",
            telegramNotice: "Этот сервис предназначен для работы внутри Telegram Mini App.",
            languageChanged: "Язык изменён.",
            hijriUnavailable: "Дата хиджры недоступна"
        }
    };

    let currentLanguage = "uz";
    let toastTimer = null;

    function getDictionary() {
        return translations[currentLanguage] || translations.uz;
    }

    function translatePage() {
        const dictionary = getDictionary();

        document.documentElement.lang = currentLanguage;

        document.querySelectorAll("[data-i18n]").forEach(element => {
            const key = element.dataset.i18n;

            if (Object.prototype.hasOwnProperty.call(dictionary, key)) {
                element.textContent = dictionary[key];
            }
        });

        document.querySelectorAll("[data-i18n-aria]").forEach(element => {
            const key = element.dataset.i18nAria;

            if (Object.prototype.hasOwnProperty.call(dictionary, key)) {
                element.setAttribute("aria-label", dictionary[key]);
            }
        });

        updateDates();
    }

    function setLanguage(language, showMessage = true) {
        if (!supportedLanguages.includes(language)) {
            language = "uz";
        }

        currentLanguage = language;

        try {
            localStorage.setItem(STORAGE_KEY, language);
        } catch (error) {
            console.warn("Language preference could not be saved.");
        }

        const selector = document.getElementById("languageSelect");

        if (selector) {
            selector.value = language;
        }

        translatePage();

        document.dispatchEvent(new CustomEvent("taqvo:languagechange", {
            detail: { language }
        }));

        if (showMessage) {
            showToast(getDictionary().languageChanged);
        }
    }

    function updateDates() {
        const now = new Date();
        const gregorian = document.getElementById("gregorianDate");
        const hijri = document.getElementById("hijriDate");

        const localeMap = {
            uz: "uz-UZ",
            "uz-Cyrl": "uz-Cyrl-UZ",
            ru: "ru-RU"
        };

        const locale = localeMap[currentLanguage] || "uz-UZ";

        if (gregorian) {
            try {
                gregorian.textContent = new Intl.DateTimeFormat(locale, {
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                }).format(now);
            } catch {
                gregorian.textContent = now.toLocaleDateString();
            }
        }

        if (hijri) {
            try {
                hijri.textContent = new Intl.DateTimeFormat(
                    locale + "-u-ca-islamic",
                    {
                        day: "numeric",
                        month: "long",
                        year: "numeric"
                    }
                ).format(now);
            } catch {
                hijri.textContent = getDictionary().hijriUnavailable;
            }
        }
    }

    function showToast(message) {
        let toast = document.getElementById("taqvoToast");

        if (!toast) {
            toast = document.createElement("div");
            toast.id = "taqvoToast";

            Object.assign(toast.style, {
                position: "fixed",
                zIndex: "9999",
                left: "50%",
                bottom: "95px",
                transform: "translateX(-50%)",
                width: "calc(100% - 40px)",
                maxWidth: "400px",
                padding: "13px 16px",
                border: "1px solid rgba(255,215,0,.3)",
                borderRadius: "13px",
                background: "#17151A",
                color: "#FFD700",
                textAlign: "center",
                fontSize: "12px",
                lineHeight: "1.5",
                boxShadow: "0 8px 30px rgba(0,0,0,.45)"
            });

            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.hidden = false;

        clearTimeout(toastTimer);

        toastTimer = setTimeout(() => {
            toast.hidden = true;
        }, 3000);
    }

    function navigateTo(action) {
        const targetMap = {
            home: "app",
            quran: "mainModules",
            tasbeeh: "mainModules",
            "taqvo-ai": "mainModules",
            profile: "dashboard-section",
            "my-quran": "dashboard-section",
            "my-khatm": "dashboard-section",
            "my-tasbeeh": "dashboard-section",
            "my-ranking": "dashboard-section",
            saved: "dashboard-section",
            "my-muhasaba": "dashboard-section",
            "my-goals": "dashboard-section",
            "my-reminders": "dashboard-section",
            "prayer-qibla": "prayer-section"
        };

        const targetId = targetMap[action];

        if (targetId === "app") {
            window.scrollTo({ top: 0, behavior: "smooth" });
            return true;
        }

        if (targetId === "dashboard-section") {
            document.querySelector(".dashboard-section")?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
            return true;
        }

        if (targetId === "prayer-section") {
            document.querySelector(".prayer-section")?.scrollIntoView({
                behavior: "smooth",
                block: "center"
            });
            return true;
        }

        if (targetId) {
            document.getElementById(targetId)?.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
            return true;
        }

        return false;
    }

    function handleAction(action) {
        const dictionary = getDictionary();

        if (action === "select-city") {
            showToast(dictionary.cityNotice);
            return;
        }

        if (action === "prayer-settings") {
            showToast(dictionary.prayerNotice);
            return;
        }

        if (action === "notifications" || action === "my-reminders") {
            showToast(dictionary.notificationNotice);
            return;
        }

        if (action === "prayer-qibla") {
            navigateTo(action);
            return;
        }

        if (action === "daily-ayah" || action === "continue-quran") {
            showToast(dictionary.soon);
            return;
        }

        if (navigateTo(action)) {
            return;
        }

        showToast(dictionary.soon);
    }

    function initTelegram() {
        const telegram = window.Telegram?.WebApp;

        if (!telegram) return;

        try {
            telegram.ready();
            telegram.expand();

            if (typeof telegram.disableVerticalSwipes === "function") {
                telegram.disableVerticalSwipes();
            }

            document.documentElement.classList.add("telegram-mini-app");
        } catch (error) {
            console.warn("Telegram Mini App initialization issue:", error);
        }
    }

    function bindEvents() {
        const selector = document.getElementById("languageSelect");

        selector?.addEventListener("change", event => {
            setLanguage(event.target.value);
        });

        document.addEventListener("click", event => {
            const target = event.target;

            if (!(target instanceof Element)) return;

            const button = target.closest("[data-action]");
            if (!button) return;

            const action = button.dataset.action;
            if (!action) return;

            if (button.classList.contains("nav-item")) {
                document.querySelectorAll(".nav-item").forEach(item => {
                    item.classList.toggle("active", item === button);
                });
            }

            handleAction(action);
        });
    }

    function init() {
        let savedLanguage = "uz";

        try {
            const stored = localStorage.getItem(STORAGE_KEY);

            if (supportedLanguages.includes(stored)) {
                savedLanguage = stored;
            }
        } catch (error) {
            console.warn("Could not read saved language.");
        }

        initTelegram();
        bindEvents();
        setLanguage(savedLanguage, false);

        console.info("TAQVO PRO MAX core initialized.");
    }

    return {
        init,
        setLanguage,
        updateDates
    };
})();

document.addEventListener("DOMContentLoaded", TAQVO.init);


/* =====================================================
   TAQVO PRO MAX — WORLDWIDE CITY & PRAYER CONNECTOR
   Version 1.2
===================================================== */

(() => {
    "use strict";

    const API = "https://taqvo-api-uz.onrender.com";

    const CITY_KEY = "taqvo_selected_city";
    const PRAYER_KEY = "taqvo_prayer_settings";

    const MADHHABS = ["hanafi", "maliki", "shafii", "hanbali"];

    const PRAYERS = ["fajr", "dhuhr", "asr", "maghrib", "isha"];

    const PRAYER_NAMES = {
        uz: {
            fajr: "Bomdod", dhuhr: "Peshin", asr: "Asr",
            maghrib: "Shom", isha: "Xufton"
        },
        "uz-Cyrl": {
            fajr: "Бомдод", dhuhr: "Пешин", asr: "Аср",
            maghrib: "Шом", isha: "Хуфтон"
        },
        ru: {
            fajr: "Фаджр", dhuhr: "Зухр", asr: "Аср",
            maghrib: "Магриб", isha: "Иша"
        }
    };

    const MESSAGES = {
        uz: {
            search: "Shahar nomini kiriting",
            searching: "Shaharlar qidirilmoqda...",
            noResults: "Shahar topilmadi.",
            error: "Xatolik yuz berdi. Qayta urinib ko‘ring.",
            choose: "Shaharni tanlang",
            failed: "Namoz vaqtlarini yuklab bo‘lmadi.",
            settings: "Namoz sozlamalari",
            hanafi: "Hanafiy",
            maliki: "Molikiy",
            shafii: "Shofe’iy",
            hanbali: "Hanbaliy",
            method: "Hisoblash usuli",
            save: "Saqlash",
            cancel: "Bekor qilish",
            invalidMethod: "Hisoblash usuli noto‘g‘ri.",
            invalidCity: "Shahar ma’lumotlari noto‘g‘ri."
        },
        "uz-Cyrl": {
            search: "Шаҳар номини киритинг",
            searching: "Шаҳарлар қидирилмоқда...",
            noResults: "Шаҳар топилмади.",
            error: "Хатолик юз берди. Қайта уриниб кўринг.",
            choose: "Шаҳарни танланг",
            failed: "Намоз вақтларини юклаб бўлмади.",
            settings: "Намоз созламалари",
            hanafi: "Ҳанафий",
            maliki: "Моликий",
            shafii: "Шофеъий",
            hanbali: "Ҳанбалий",
            method: "Ҳисоблаш усули",
            save: "Сақлаш",
            cancel: "Бекор қилиш",
            invalidMethod: "Ҳисоблаш усули нотўғри.",
            invalidCity: "Шаҳар маълумотлари нотўғри."
        },
        ru: {
            search: "Введите название города",
            searching: "Поиск городов...",
            noResults: "Город не найден.",
            error: "Произошла ошибка. Попробуйте ещё раз.",
            choose: "Выберите город",
            failed: "Не удалось загрузить время намаза.",
            settings: "Настройки намаза",
            hanafi: "Ханафитский",
            maliki: "Маликитский",
            shafii: "Шафиитский",
            hanbali: "Ханбалитский",
            method: "Метод расчёта",
            save: "Сохранить",
            cancel: "Отмена",
            invalidMethod: "Неверный метод расчёта.",
            invalidCity: "Некорректные данные города."
        }
    };

    let selectedCity = null;
    let prayerData = null;

    let countdownTimer = null;
    let searchTimer = null;

    let searchController = null;
    let prayerController = null;

    let searchSequence = 0;
    let prayerSequence = 0;

    let lastActivePrayer = null;
    let lastCityDate = null;

    /* ---------------- LANGUAGE ---------------- */

    function language() {
        const value = document.getElementById("languageSelect")?.value;
        return MESSAGES[value] ? value : "uz";
    }

    function t(key) {
        return MESSAGES[language()][key] || key;
    }

    function prayerNames() {
        return PRAYER_NAMES[language()] || PRAYER_NAMES.uz;
    }

    /* ---------------- NOTIFICATION ---------------- */

    function notify(message) {
        let toast = document.getElementById("taqvoToast");

        if (!toast) {
            toast = document.createElement("div");
            toast.id = "taqvoToast";

            Object.assign(toast.style, {
                position: "fixed",
                zIndex: "20000",
                left: "50%",
                bottom: "95px",
                transform: "translateX(-50%)",
                width: "calc(100% - 40px)",
                maxWidth: "400px",
                padding: "13px 16px",
                border: "1px solid rgba(255,215,0,.3)",
                borderRadius: "13px",
                background: "#17151A",
                color: "#FFD700",
                textAlign: "center",
                fontSize: "13px",
                lineHeight: "1.5",
                boxShadow: "0 8px 30px rgba(0,0,0,.45)"
            });

            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.hidden = false;

        clearTimeout(notify.timer);

        notify.timer = setTimeout(() => {
            toast.hidden = true;
        }, 3000);
    }

    /* ---------------- STORAGE ---------------- */

    function readStorage(key, fallback = null) {
        try {
            const value = localStorage.getItem(key);
            return value ? JSON.parse(value) : fallback;
        } catch (error) {
            console.warn("TAQVO storage read error:", error);
            return fallback;
        }
    }

    function writeStorage(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (error) {
            console.warn("TAQVO storage write error:", error);
            notify(t("error"));
            return false;
        }
    }

    /* ---------------- CITY VALIDATION ---------------- */

    function normalizeCity(city) {
        if (!city || typeof city !== "object") return null;

        const latitude = Number(city.latitude ?? city.lat);
        const longitude = Number(city.longitude ?? city.lon);
        const timezone = String(city.timezone || "").trim();

        if (
            !Number.isFinite(latitude) ||
            latitude < -90 || latitude > 90 ||
            !Number.isFinite(longitude) ||
            longitude < -180 || longitude > 180 ||
            !timezone
        ) {
            return null;
        }

        try {
            new Intl.DateTimeFormat("en", {
                timeZone: timezone
            }).format(new Date());
        } catch {
            return null;
        }

        return {
            id: city.id ?? null,
            name: String(city.name || ""),
            country: String(city.country || ""),
            country_code: city.country_code || "",
            region: city.region || "",
            latitude,
            longitude,
            timezone
        };
    }

    /* ---------------- PRAYER SETTINGS ---------------- */

    function getPrayerSettings() {
        const saved = readStorage(PRAYER_KEY, {});

        const madhhab = MADHHABS.includes(saved?.madhhab)
            ? saved.madhhab
            : "hanafi";

        const method = Number(saved?.method);

        return {
            madhhab,
            method: Number.isInteger(method) &&
                ((method >= 0 && method <= 23) || method === 99)
                ? method
                : 3
        };
    }

    function saveMadhhab(value) {
        if (!MADHHABS.includes(value)) return;

        const settings = getPrayerSettings();

        writeStorage(PRAYER_KEY, {
            method: settings.method,
            madhhab: value
        });

        if (selectedCity) loadPrayerTimes();

        notify(t(value));
    }

    function initMadhhabSelector() {
        const selector = document.getElementById("madhhabSelect");

        if (!selector) {
            console.warn("TAQVO: madhhabSelect not found.");
            return;
        }

        selector.value = getPrayerSettings().madhhab;

        selector.addEventListener("change", () => {
            saveMadhhab(selector.value);
        });
    }

    /* ---------------- CITY MODAL STYLES ---------------- */

    function addModalStyles() {
        if (document.getElementById("taqvo-city-styles")) return;

        const style = document.createElement("style");
        style.id = "taqvo-city-styles";

        style.textContent = `
            #taqvoCityModal {
                position: fixed;
                inset: 0;
                z-index: 10000;
                display: none;
                align-items: center;
                justify-content: center;
                padding: 18px;
                background: rgba(0,0,0,.82);
                backdrop-filter: blur(12px);
            }

            #taqvoCityModal.open {
                display: flex;
            }

            .taqvo-city-box {
                width: 100%;
                max-width: 440px;
                max-height: 85vh;
                overflow-y: auto;
                padding: 22px;
                border: 1px solid rgba(255,215,0,.35);
                border-radius: 22px;
                background: #111014;
                color: #fff;
                box-shadow: 0 15px 60px #000;
            }

            .taqvo-city-box h2 {
                margin: 0 0 18px;
                color: #FFD700;
                font-size: 21px;
            }

            #taqvoCitySearch {
                width: 100%;
                box-sizing: border-box;
                padding: 15px;
                border: 1px solid rgba(255,215,0,.35);
                border-radius: 12px;
                outline: none;
                background: #201d20;
                color: white;
                font-size: 16px;
            }

            #taqvoCityResults {
                margin-top: 14px;
                display: grid;
                gap: 9px;
            }

            .taqvo-city-result {
                width: 100%;
                padding: 14px;
                border: 1px solid rgba(255,215,0,.16);
                border-radius: 12px;
                background: #1c191c;
                color: white;
                text-align: left;
                font-size: 15px;
            }

            .taqvo-city-result small {
                display: block;
                margin-top: 5px;
                color: #aaa;
            }

            .taqvo-city-close {
                width: 100%;
                margin-top: 15px;
                padding: 13px;
                border: 1px solid #555;
                border-radius: 12px;
                background: transparent;
                color: white;
                font-size: 15px;
            }

            #taqvoCityStatus {
                margin-top: 12px;
                color: #FFD700;
                font-size: 13px;
            }
        `;

        document.head.appendChild(style);
    }

    /* ---------------- CITY MODAL ---------------- */

    function createModal() {
        if (document.getElementById("taqvoCityModal")) return;

        addModalStyles();

        const modal = document.createElement("div");
        modal.id = "taqvoCityModal";

        const box = document.createElement("div");
        box.className = "taqvo-city-box";

        const heading = document.createElement("h2");
        heading.textContent = "📍 " + t("choose");

        const input = document.createElement("input");
        input.id = "taqvoCitySearch";
        input.type = "search";
        input.placeholder = t("search");
        input.autocomplete = "off";

        const status = document.createElement("div");
        status.id = "taqvoCityStatus";

        const results = document.createElement("div");
        results.id = "taqvoCityResults";

        const closeButton = document.createElement("button");
        closeButton.type = "button";
        closeButton.className = "taqvo-city-close";
        closeButton.id = "taqvoCityClose";
        closeButton.textContent = t("cancel");

        box.append(heading, input, status, results, closeButton);
        modal.appendChild(box);
        document.body.appendChild(modal);

        modal.addEventListener("click", event => {
            if (event.target === modal) closeCityModal();
        });

        closeButton.addEventListener("click", closeCityModal);

        input.addEventListener("input", event => {
            const query = event.target.value.trim();

            clearTimeout(searchTimer);

            if (searchController) {
                searchController.abort();
                searchController = null;
            }

            searchSequence++;

            if (query.length < 2) {
                results.replaceChildren();
                status.textContent = "";
                return;
            }

            searchTimer = setTimeout(() => searchCities(query), 400);
        });
    }

    function openCityModal() {
        createModal();

        const modal = document.getElementById("taqvoCityModal");
        const input = document.getElementById("taqvoCitySearch");

        modal.querySelector("h2").textContent = "📍 " + t("choose");
        input.placeholder = t("search");

        modal.classList.add("open");

        setTimeout(() => input.focus(), 150);
    }

    function closeCityModal() {
        document.getElementById("taqvoCityModal")
            ?.classList.remove("open");

        if (searchController) {
            searchController.abort();
            searchController = null;
        }
    }

    /* ---------------- CITY SEARCH API ---------------- */

    async function searchCities(query) {
        const status = document.getElementById("taqvoCityStatus");
        const results = document.getElementById("taqvoCityResults");

        const sequence = ++searchSequence;

        if (searchController) searchController.abort();

        searchController = new AbortController();

        status.textContent = t("searching");
        results.replaceChildren();

        try {
            const url = new URL(API + "/api/prayer/cities");

            url.searchParams.set("q", query);
            url.searchParams.set("count", "15");
            url.searchParams.set(
                "language",
                language() === "ru" ? "ru" : "en"
            );

            const response = await fetch(url, {
                signal: searchController.signal
            });

            if (!response.ok) {
                throw new Error("City search HTTP " + response.status);
            }

            const data = await response.json();

            if (sequence !== searchSequence) return;

            if (!Array.isArray(data.results) || !data.results.length) {
                status.textContent = t("noResults");
                return;
            }

            status.textContent = "";

            data.results.forEach(rawCity => {
                const city = normalizeCity(rawCity);
                if (!city) return;

                const button = document.createElement("button");
                button.type = "button";
                button.className = "taqvo-city-result";

                const title = document.createElement("strong");
                title.textContent = city.name;

                const subtitle = document.createElement("small");
                subtitle.textContent = [
                    city.region,
                    city.country
                ].filter(Boolean).join(", ");

                button.append(title, subtitle);

                button.addEventListener("click", () => {
                    selectCity(city);
                });

                results.appendChild(button);
            });

            if (!results.children.length) {
                status.textContent = t("noResults");
            }

        } catch (error) {
            if (error.name === "AbortError") return;
            if (sequence !== searchSequence) return;

            console.error("TAQVO city search:", error);
            status.textContent = t("error");
        }
    }

    /* ---------------- SELECT CITY ---------------- */

    async function selectCity(rawCity) {
        const city = normalizeCity(rawCity);

        if (!city) {
            notify(t("invalidCity"));
            return;
        }

        selectedCity = city;
        prayerData = null;
        lastCityDate = null;
        lastActivePrayer = null;

        writeStorage(CITY_KEY, city);

        updateLocationName();
        closeCityModal();

        await loadPrayerTimes();
    }

    function updateLocationName() {
        const location = document.getElementById("userLocation");

        if (!location || !selectedCity) return;

        location.textContent = [
            selectedCity.name,
            selectedCity.country
        ].filter(Boolean).join(", ");
    }

    /* ---------------- CITY CLOCK ---------------- */

    function getCityDateKey() {
        if (!selectedCity) return null;

        const parts = new Intl.DateTimeFormat("en-GB", {
            timeZone: selectedCity.timezone,
            year: "numeric",
            month: "2-digit",
            day: "2-digit"
        }).formatToParts(new Date());

        const values = {};

        parts.forEach(part => {
            values[part.type] = part.value;
        });

        return `${values.year}-${values.month}-${values.day}`;
    }

    function getCityClock() {
        const parts = new Intl.DateTimeFormat("en-GB", {
            timeZone: selectedCity.timezone,
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hourCycle: "h23"
        }).formatToParts(new Date());

        const values = {};

        parts.forEach(part => {
            values[part.type] = part.value;
        });

        return {
            hour: Number(values.hour),
            minute: Number(values.minute),
            second: Number(values.second)
        };
    }

    /* ---------------- LOAD PRAYER TIMES ---------------- */

    async function loadPrayerTimes() {
        if (!selectedCity) return;

        if (prayerController) {
            prayerController.abort();
        }

        prayerController = new AbortController();

        const sequence = ++prayerSequence;
        const settings = getPrayerSettings();

        const url = new URL(API + "/api/prayer/today");

        url.searchParams.set("latitude", String(selectedCity.latitude));
        url.searchParams.set("longitude", String(selectedCity.longitude));
        url.searchParams.set("timezone", selectedCity.timezone);
        url.searchParams.set("method", String(settings.method));

        // Backend expects madhhab.
        // Do not send the old school parameter.
        url.searchParams.set("madhhab", settings.madhhab);

        try {
            const response = await fetch(url, {
                signal: prayerController.signal
            });

            if (!response.ok) {
                throw new Error("Prayer API HTTP " + response.status);
            }

            const data = await response.json();

            if (sequence !== prayerSequence) return;

            if (
                !data.success ||
                !data.timings ||
                !PRAYERS.every(key => data.timings[key])
            ) {
                throw new Error("Invalid prayer API response");
            }

            prayerData = data;
            lastCityDate = getCityDateKey();
            lastActivePrayer = null;

            renderPrayerTimes();
            updateCityDates();

        } catch (error) {
            if (error.name === "AbortError") return;
            if (sequence !== prayerSequence) return;

            console.error("TAQVO prayer API:", error);
            notify(t("failed"));
        }
    }

    /* ---------------- RENDER PRAYER TIMES ---------------- */

    function renderPrayerTimes() {
        if (!prayerData?.timings) return;

        PRAYERS.forEach(key => {
            const item = document.querySelector(
                `.prayer-item[data-prayer="${key}"]`
            );

            if (!item) return;

            const strong = item.querySelector("strong");
            const value = prayerData.timings[key] || "--:--";

            if (strong && strong.textContent !== value) {
                strong.textContent = value;
            }
        });

        updateNextPrayer();
    }

    /* ---------------- PARSE PRAYER TIME ---------------- */

    function parsePrayerTime(value) {
        if (typeof value !== "string") return null;

        const match = value.trim().match(/^(\d{1,2}):(\d{2})/);
        if (!match) return null;

        const hour = Number(match[1]);
        const minute = Number(match[2]);

        if (
            hour < 0 || hour > 23 ||
            minute < 0 || minute > 59
        ) {
            return null;
        }

        return hour * 3600 + minute * 60;
    }

    /* ---------------- NEXT PRAYER ---------------- */

    function updateNextPrayer() {
    if (!prayerData?.timings || !selectedCity) return;

    const clock = getCityClock();

    const nowSeconds =
        clock.hour * 3600 +
        clock.minute * 60 +
        clock.second;

    let nextPrayer = null;
    let difference = null;

    for (const key of PRAYERS) {
        const prayerSeconds = parsePrayerTime(
            prayerData.timings[key]
        );

        if (prayerSeconds === null) continue;

        if (prayerSeconds > nowSeconds) {
            nextPrayer = key;
            difference = prayerSeconds - nowSeconds;
            break;
        }
    }

    if (!nextPrayer) {
        const fajrSeconds = parsePrayerTime(
            prayerData.timings.fajr
        );

        if (fajrSeconds === null) return;

        nextPrayer = "fajr";
        difference = 86400 - nowSeconds + fajrSeconds;
    }

    const nextName = document.getElementById("nextPrayerName");
    const countdown = document.getElementById("nextPrayerCountdown");

    if (nextName) {
        const name = prayerNames()[nextPrayer];

        if (nextName.textContent !== name) {
            nextName.textContent = name;
        }
    }

    if (countdown) {
        const totalMinutes = Math.ceil(difference / 60);
        const h = Math.floor(totalMinutes / 60);
        const m = totalMinutes % 60;

        const value =
            String(h).padStart(2, "0") + ":" +
            String(m).padStart(2, "0");

        if (countdown.textContent !== value) {
            countdown.textContent = value;
        }
    }

    if (lastActivePrayer !== nextPrayer) {
        document.querySelectorAll(".prayer-item").forEach(item => {
            item.classList.toggle(
                "active",
                item.dataset.prayer === nextPrayer
            );
        });

        lastActivePrayer = nextPrayer;
    }
}
