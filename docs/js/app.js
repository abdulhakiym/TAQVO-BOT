"use strict";

/* =====================================================
   TAQVO PRO MAX — APPLICATION CORE
   Version 1.1
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
            fajr: "Bomdod",
            dhuhr: "Peshin",
            asr: "Asr",
            maghrib: "Shom",
            isha: "Xufton",
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
            fajr: "Бомдод",
            dhuhr: "Пешин",
            asr: "Аср",
            maghrib: "Шом",
            isha: "Хуфтон",
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
            fajr: "Фаджр",
            dhuhr: "Зухр",
            asr: "Аср",
            maghrib: "Магриб",
            isha: "Иша",
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

        document.documentElement.lang =
            currentLanguage === "uz-Cyrl" ? "uz-Cyrl" : currentLanguage;

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
            } catch (error) {
                gregorian.textContent = now.toLocaleDateString();
            }
        }

        if (hijri) {
            try {
                const hijriLocale = locale + "-u-ca-islamic";

                hijri.textContent = new Intl.DateTimeFormat(
                    hijriLocale,
                    {
                        day: "numeric",
                        month: "long",
                        year: "numeric"
                    }
                ).format(now);
            } catch (error) {
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
                zIndex: "999",
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
            showToast(dictionary.prayerNotice);
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

        if (!telegram) {
            return;
        }

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

            if (!(target instanceof Element)) {
                return;
            }

            const button = target.closest("[data-action]");

            if (!button) {
                return;
            }

            const action = button.dataset.action;

            if (!action) {
                return;
            }

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

        console.info("TAQVO PRO MAX initialized successfully.");
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
   Backend: taqvo-api-uz.onrender.com
===================================================== */

(() => {
    "use strict";

    const API = "https://taqvo-api-uz.onrender.com";
    const CITY_KEY = "taqvo_selected_city";
    const PRAYER_KEY = "taqvo_prayer_settings";

    const prayerNames = {
        uz: {
            fajr: "Bomdod",
            dhuhr: "Peshin",
            asr: "Asr",
            maghrib: "Shom",
            isha: "Xufton"
        },
        "uz-Cyrl": {
            fajr: "Бомдод",
            dhuhr: "Пешин",
            asr: "Аср",
            maghrib: "Шом",
            isha: "Хуфтон"
        },
        ru: {
            fajr: "Фаджр",
            dhuhr: "Зухр",
            asr: "Аср",
            maghrib: "Магриб",
            isha: "Иша"
        }
    };

    const messages = {
        uz: {
            search: "Shahar nomini kiriting",
            searching: "Shaharlar qidirilmoqda...",
            noResults: "Shahar topilmadi.",
            error: "Xatolik yuz berdi. Qayta urinib ko‘ring.",
            choose: "Shaharni tanlang",
            loading: "Namoz vaqtlari yuklanmoqda...",
            failed: "Namoz vaqtlarini yuklab bo‘lmadi.",
            settings: "Namoz sozlamalari",
            hanafi: "Hanafiy",
            shafii: "Shofe’iy",
            method: "Hisoblash usuli",
            save: "Saqlash",
            cancel: "Bekor qilish",
            next: "Keyingi namoz",
            today: "Bugungi namoz vaqtlari"
        },
        "uz-Cyrl": {
            search: "Шаҳар номини киритинг",
            searching: "Шаҳарлар қидирилмоқда...",
            noResults: "Шаҳар топилмади.",
            error: "Хатолик юз берди. Қайта уриниб кўринг.",
            choose: "Шаҳарни танланг",
            loading: "Намоз вақтлари юкланмоқда...",
            failed: "Намоз вақтларини юклаб бўлмади.",
            settings: "Намоз созламалари",
            hanafi: "Ҳанафий",
            shafii: "Шофеъий",
            method: "Ҳисоблаш усули",
            save: "Сақлаш",
            cancel: "Бекор қилиш",
            next: "Кейинги намоз",
            today: "Бугунги намоз вақтлари"
        },
        ru: {
            search: "Введите название города",
            searching: "Поиск городов...",
            noResults: "Город не найден.",
            error: "Произошла ошибка. Попробуйте ещё раз.",
            choose: "Выберите город",
            loading: "Загрузка времени намаза...",
            failed: "Не удалось загрузить время намаза.",
            settings: "Настройки намаза",
            hanafi: "Ханафитский",
            shafii: "Шафиитский",
            method: "Метод расчёта",
            save: "Сохранить",
            cancel: "Отмена",
            next: "Следующий намаз",
            today: "Время намаза на сегодня"
        }
    };

    let selectedCity = null;
    let prayerData = null;
    let countdownTimer = null;
    let searchTimer = null;
    let searchRequest = null;

    const language = () => {
        const value = document.getElementById("languageSelect")?.value;
        return messages[value] ? value : "uz";
    };

    const t = (key) => messages[language()][key];

    const names = () => prayerNames[language()];

    function notify(message) {
        if (window.TAQVO?.showToast) {
            window.TAQVO.showToast(message);
            return;
        }

        const toast = document.getElementById("taqvoToast");

        if (toast) {
            toast.textContent = message;
            toast.hidden = false;
            setTimeout(() => {
                toast.hidden = true;
            }, 3000);
        } else {
            alert(message);
        }
    }

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

    function createModal() {
        if (document.getElementById("taqvoCityModal")) return;

        addModalStyles();

        const modal = document.createElement("div");
        modal.id = "taqvoCityModal";

        modal.innerHTML = `
            <div class="taqvo-city-box">
                <h2>📍 ${t("choose")}</h2>
                <input
                    id="taqvoCitySearch"
                    type="search"
                    placeholder="${t("search")}"
                    autocomplete="off"
                >
                <div id="taqvoCityStatus"></div>
                <div id="taqvoCityResults"></div>
                <button class="taqvo-city-close" id="taqvoCityClose">
                    ${t("cancel")}
                </button>
            </div>
        `;

        document.body.appendChild(modal);

        modal.addEventListener("click", event => {
            if (event.target === modal) closeCityModal();
        });

        document.getElementById("taqvoCityClose")
            .addEventListener("click", closeCityModal);

        document.getElementById("taqvoCitySearch")
            .addEventListener("input", event => {
                const query = event.target.value.trim();

                clearTimeout(searchTimer);

                if (searchRequest) {
                    searchRequest.abort();
                }

                if (query.length < 2) {
                    document.getElementById("taqvoCityResults").innerHTML = "";
                    document.getElementById("taqvoCityStatus").textContent = "";
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
    }

    async function searchCities(query) {
        const status = document.getElementById("taqvoCityStatus");
        const results = document.getElementById("taqvoCityResults");

        status.textContent = t("searching");
        results.innerHTML = "";

        searchRequest = new AbortController();

        const languageCode = language() === "ru" ? "ru" : "en";

        try {
            const url = new URL(API + "/api/prayer/cities");

            url.searchParams.set("q", query);
            url.searchParams.set("count", "15");
            url.searchParams.set("language", languageCode);

            const response = await fetch(url, {
                signal: searchRequest.signal
            });

            if (!response.ok) throw new Error("City search failed");

            const data = await response.json();

            if (!data.results?.length) {
                status.textContent = t("noResults");
                return;
            }

            status.textContent = "";

            data.results.forEach(city => {
                const button = document.createElement("button");

                button.className = "taqvo-city-result";

                const title = document.createElement("strong");
                title.textContent = city.name || "";

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

        } catch (error) {
            if (error.name === "AbortError") return;

            console.error("TAQVO city search:", error);
            status.textContent = t("error");
        }
    }

    async function selectCity(city) {
        selectedCity = city;

        localStorage.setItem(CITY_KEY, JSON.stringify(city));

        const location = document.getElementById("userLocation");

        if (location) {
            location.textContent = [
                city.name,
                city.country
            ].filter(Boolean).join(", ");
        }

        closeCityModal();

        await loadPrayerTimes();
    }

    function getPrayerSettings() {
        try {
            return JSON.parse(localStorage.getItem(PRAYER_KEY)) || {
                method: 3,
                school: 1
            };
        } catch {
            return { method: 3, school: 1 };
        }
    }

    async function loadPrayerTimes() {
        if (!selectedCity) return;

        notify(t("loading"));

        const settings = getPrayerSettings();

        const url = new URL(API + "/api/prayer/today");

        url.searchParams.set("latitude", selectedCity.latitude);
        url.searchParams.set("longitude", selectedCity.longitude);
        url.searchParams.set("timezone", selectedCity.timezone);
        url.searchParams.set("method", settings.method);
        url.searchParams.set("school", settings.school);

        try {
            const response = await fetch(url);

            if (!response.ok) throw new Error("Prayer API failed");

            prayerData = await response.json();

            if (!prayerData.success) throw new Error("Invalid response");

            renderPrayerTimes();
            updateCityDates();

            notify(t("today"));

        } catch (error) {
            console.error("TAQVO prayer times:", error);
            notify(t("failed"));
        }
    }

    function renderPrayerTimes() {
        if (!prayerData?.timings) return;

        Object.entries(prayerData.timings).forEach(([key, value]) => {
            const item = document.querySelector(
                `.prayer-item[data-prayer="${key}"]`
            );

            if (!item) return;

            const strong = item.querySelector("strong");

            if (strong) strong.textContent = value || "--:--";
        });

        const hijri = document.getElementById("hijriDate");

        if (hijri && prayerData.hijri?.date) {
            const h = prayerData.hijri;
            hijri.textContent = [
                h.day,
                h.month?.en,
                h.year,
                "AH"
            ].filter(Boolean).join(" ");
        }

        updateNextPrayer();
    }

    function getCityClock() {
        const parts = new Intl.DateTimeFormat("en-GB", {
            timeZone: selectedCity.timezone,
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hourCycle: "h23"
        }).formatToParts(new Date());

        const result = {};

        parts.forEach(part => {
            result[part.type] = part.value;
        });

        return {
            hour: Number(result.hour),
            minute: Number(result.minute),
            second: Number(result.second)
        };
    }

    function updateNextPrayer() {
        if (!prayerData?.timings || !selectedCity) return;

        const order = ["fajr", "dhuhr", "asr", "maghrib", "isha"];
        const clock = getCityClock();

        const nowSeconds =
            clock.hour * 3600 +
            clock.minute * 60 +
            clock.second;

        let next = null;
        let difference = 0;

        for (const key of order) {
            const value = prayerData.timings[key];

            if (!value) continue;

            const [hour, minute] = value.split(":").map(Number);
            const prayerSeconds = hour * 3600 + minute * 60;

            if (prayerSeconds > nowSeconds) {
                next = key;
                difference = prayerSeconds - nowSeconds;
                break;
            }
        }

        if (!next) {
            next = "fajr";

            const [hour, minute] =
                prayerData.timings.fajr.split(":").map(Number);

            difference =
                86400 - nowSeconds + hour * 3600 + minute * 60;
        }

        document.getElementById("nextPrayerName").textContent =
            names()[next];

        const h = Math.floor(difference / 3600);
        const m = Math.floor((difference % 3600) / 60);
        const s = difference % 60;

        document.getElementById("nextPrayerCountdown").textContent =
            [h, m, s].map(value => String(value).padStart(2, "0")).join(":");

        document.querySelectorAll(".prayer-item").forEach(item => {
            item.classList.toggle(
                "active",
                item.dataset.prayer === next
            );
        });
    }

    function updateCityDates() {
        if (!selectedCity) return;

        const now = new Date();

        const localeMap = {
            uz: "uz-UZ",
            "uz-Cyrl": "uz-Cyrl-UZ",
            ru: "ru-RU"
        };

        const locale = localeMap[language()];

        const gregorian = document.getElementById("gregorianDate");

        if (gregorian) {
            gregorian.textContent = new Intl.DateTimeFormat(locale, {
                day: "numeric",
                month: "long",
                year: "numeric",
                timeZone: selectedCity.timezone
            }).format(now);
        }
    }

    function openPrayerSettings() {
        const settings = getPrayerSettings();

        const methodInput = prompt(
            t("method") + "\n0–23 yoki 99",
            String(settings.method)
        );

        if (methodInput === null) return;

        const method = Number(methodInput);

        if (!Number.isInteger(method) ||
            !((method >= 0 && method <= 23) || method === 99)) {
            notify(t("error"));
            return;
        }

        const schoolInput = prompt(
            t("hanafi") + " = 1\n" + t("shafii") + " = 0",
            String(settings.school)
        );

        if (schoolInput === null) return;

        const school = Number(schoolInput);

        if (![0, 1].includes(school)) {
            notify(t("error"));
            return;
        }

        localStorage.setItem(PRAYER_KEY, JSON.stringify({
            method,
            school
        }));

        loadPrayerTimes();
    }

    function handleConnectorClick(event) {
        const target = event.target;

        if (!(target instanceof Element)) return;

        const button = target.closest("[data-action]");

        if (!button) return;

        const action = button.dataset.action;

        if (action === "select-city") {
            event.preventDefault();
            event.stopImmediatePropagation();
            openCityModal();
        }

        if (action === "prayer-settings") {
            event.preventDefault();
            event.stopImmediatePropagation();
            openPrayerSettings();
        }
    }

    function init() {
        document.addEventListener("click", handleConnectorClick, true);

        try {
            const saved = localStorage.getItem(CITY_KEY);

            if (saved) {
                selectedCity = JSON.parse(saved);

                const location = document.getElementById("userLocation");

                if (location) {
                    location.textContent = [
                        selectedCity.name,
                        selectedCity.country
                    ].filter(Boolean).join(", ");
                }

                loadPrayerTimes();
            }
        } catch (error) {
            console.warn("TAQVO saved city could not be loaded.");
        }

        if (countdownTimer) clearInterval(countdownTimer);

        countdownTimer = setInterval(() => {
            if (prayerData) updateNextPrayer();
        }, 1000);

        document.getElementById("languageSelect")
            ?.addEventListener("change", () => {
                if (selectedCity) {
                    updateCityDates();
                    renderPrayerTimes();
                }
            });

        console.info("TAQVO worldwide prayer connector initialized.");
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init, { once: true });
    } else {
        init();
    }
})();

