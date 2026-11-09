
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)


CHANNEL_USERNAME = "@hakiymqalb"
CHANNEL_URL = "https://t.me/hakiymqalb"


# ==========================================
# 1. KANALGA OBUNA BO'LISH
# ==========================================

def subscription_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 KANALGA OBUNA BO'LISH",
                    url=CHANNEL_URL,
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ OBUNANI TASDIQLASH",
                    callback_data="subscription:check",
                )
            ],
        ]
    )


# ==========================================
# 2. JOYLASHUVNI TANLASH
# ==========================================

def location_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="📍 GPS ORQALI ANIQLASH",
                    request_location=True,
                )
            ],
            [
                KeyboardButton(
                    text="🌍 DAVLAT VA SHAHARNI TANLASH"
                )
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# ==========================================
# 3. DAVLATLARNI TANLASH
# ==========================================

def countries_keyboard() -> InlineKeyboardMarkup:
    countries = [
        ("🇺🇿 O‘zbekiston", "UZ"),
        ("🇰🇿 Qozog‘iston", "KZ"),
        ("🇷🇺 Rossiya", "RU"),
        ("🇹🇷 Turkiya", "TR"),
        ("🇸🇦 Saudiya Arabistoni", "SA"),
    ]

    buttons = [
        [
            InlineKeyboardButton(
                text=name,
                callback_data=f"country:{code}",
            )
        ]
        for name, code in countries
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ==========================================
# 4. SHAHARLARNI TANLASH
# ==========================================

CITIES = {
    "UZ": [
        ("Toshkent", "tashkent"),
        ("Samarqand", "samarkand"),
        ("Farg‘ona", "fergana"),
        ("Andijon", "andijan"),
        ("Namangan", "namangan"),
    ],
    "KZ": [
        ("Olmaota", "almaty"),
        ("Ostona", "astana"),
        ("Temirtau", "temirtau"),
        ("Qarag‘anda", "karaganda"),
    ],
    "RU": [
        ("Moskva", "moscow"),
        ("Sankt-Peterburg", "saint-petersburg"),
    ],
    "TR": [
        ("Istanbul", "istanbul"),
        ("Anqara", "ankara"),
    ],
    "SA": [
        ("Makka", "makkah"),
        ("Madina", "madinah"),
        ("Jidda", "jeddah"),
    ],
}


def cities_keyboard(country_code: str) -> InlineKeyboardMarkup:
    cities = CITIES.get(country_code, [])

    buttons = [
        [
            InlineKeyboardButton(
                text=name,
                callback_data=f"city:{country_code}:{slug}",
            )
        ]
        for name, slug in cities
    ]

    buttons.append(
        [
            InlineKeyboardButton(
                text="⬅️ DAVLATLARGA QAYTISH",
                callback_data="location:countries",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


# ==========================================
# 5. MINI APP'NI OCHISH
# ==========================================

def mini_app_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    if not webapp_url.startswith("https://"):
        raise ValueError(
            "Telegram Mini App uchun HTTPS manzil kerak."
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 TAQVO PRO MAX ILOVASINI OCHISH",
                    web_app=WebAppInfo(url=webapp_url),
                )
            ]
        ]
    )


# ==========================================
# 6. ORQAGA QAYTISH
# ==========================================

def back_to_countries_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ ORQAGA",
                    callback_data="location:countries",
                )
            ]
        ]
    )
