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
