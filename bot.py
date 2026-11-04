import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from config import settings
from database import (
    init_db,
    close_db,
    save_user,
    get_user,
    save_city,
    set_subscription,
)

from keyboards import (
    subscription_keyboard,
    country_keyboard,
    city_search_keyboard,
    city_results_keyboard,
    mini_app_keyboard,
)

from prayer_times import (
    search_cities,
    get_prayer_times,
    format_prayer_times,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)

dp = Dispatcher(storage=MemoryStorage())

# Vaqtincha qidiruv natijalari.
# Bot qayta ishga tushganda ular yangidan olinadi.
city_cache: dict[int, dict[str, dict]] = {}


def prayer_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🕌 Namoz vaqtlarim"),
            ],
            [
                KeyboardButton(text="🚀 TAQVO PRO MAX"),
            ],
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


async def check_subscription(user_id: int) -> bool:
    member = await bot.get_chat_member(
        chat_id=settings.CHANNEL_USERNAME,
        user_id=user_id,
    )

    return member.status in {
        "member",
        "administrator",
        "creator",
    }


async def show_subscription(message: Message):
    await message.answer(
        "🤲 TAQVO PRO MAX xizmatidan foydalanish uchun "
        "avval rasmiy kanalimizga obuna bo‘ling.\n\n"
        "Obuna bo‘lgach, tasdiqlash tugmasini bosing.",
        reply_markup=subscription_keyboard(),
    )


async def welcome_user(message: Message):
    user = message.from_user
    name = user.first_name or "aziz birodar"

    await message.answer(
        "Assalomu alaykum va rohmatullohi va barokatuh! 🤲\n\n"
        f"Xush kelibsiz, {name}!\n\n"
        "Sizga mos namoz vaqtlarini ko‘rsatish uchun "
        "davlatingiz va shahringizni tanlang."
    )

    await message.answer(
        "🌍 Davlatingizni tanlang:",
        reply_markup=country_keyboard(),
    )


@dp.message(CommandStart())
async def start(message: Message):
    user = message.from_user

    await save_user(
        user_id=user.id,
        first_name=user.first_name or "",
        username=user.username,
    )

    try:
        subscribed = await check_subscription(user.id)
    except Exception:
        logger.exception("Obunani tekshirishda xatolik")
        await message.answer(
            "Kanal obunasini hozir tekshira olmadik. "
            "Iltimos, birozdan keyin qayta urinib ko‘ring."
        )
        return

    if not subscribed:
        await show_subscription(message)
        return

    await set_subscription(user.id, True)

    profile = await get_user(user.id)

    if profile and profile.get("city"):
        await send_prayer_times(message, profile)
        return

    await welcome_user(message)


@dp.callback_query(F.data == "subscription:check")
async def verify_subscription(callback: CallbackQuery):
    try:
        subscribed = await check_subscription(
            callback.from_user.id
        )
    except Exception:
        logger.exception("Obunani qayta tekshirishda xatolik")
        await callback.answer(
            "Tekshirish imkoni bo‘lmadi.",
            show_alert=True,
        )
        return

    if not subscribed:
        await callback.answer(
            "Avval kanalga obuna bo‘ling.",
            show_alert=True,
        )
        return

    await set_subscription(callback.from_user.id, True)

    await callback.answer("Obuna tasdiqlandi!")

    try:
        await callback.message.delete()
    except Exception:
        pass

    user = callback.from_user
    await callback.bot.send_message(
        user.id,
        "Assalomu alaykum va rohmatullohi va barokatuh! 🤲\n\n"
        f"Xush kelibsiz, {user.first_name or 'aziz birodar'}!\n\n"
        "Davlatingizni tanlang:",
        reply_markup=country_keyboard(),
    )


@dp.callback_query(F.data.startswith("country:"))
async def choose_country(callback: CallbackQuery):
    country_code = callback.data.split(":", 1)[1]

    if country_code == "other":
        await callback.answer()
        await callback.message.answer(
            "Davlat yoki shahar nomini yozing. "
            "Masalan: London, Tokyo, Berlin."
        )
        return

    await callback.answer()

    await callback.message.answer(
        "🔎 Endi shahringiz nomini yozing:"
    )


@dp.message(F.text)
async def handle_text(message: Message):
    text = message.text.strip()
    user_id = message.from_user.id

    if text == "🕌 Namoz vaqtlarim":
        profile = await get_user(user_id)

        if not profile or not profile.get("city"):
            await message.answer(
                "Avval shahringizni tanlang."
            )
            await welcome_user(message)
            return

        await send_prayer_times(message, profile)
        return

    if text == "🚀 TAQVO PRO MAX":
        try:
            await message.answer(
                "Barcha imkoniyatlardan foydalanish uchun "
                "ilovani oching:",
                reply_markup=mini_app_keyboard(),
            )
        except RuntimeError:
            await message.answer(
                "Mini App manzili hali sozlanmagan."
            )
        return

    try:
        cities = await search_cities(text)
    except Exception:
        logger.exception("Shahar qidiruvida xatolik")
        await message.answer(
            "Shaharlarni qidirishda xatolik yuz berdi. "
            "Qayta urinib ko‘ring."
        )
        return

    if not cities:
        await message.answer(
            "Shahar topilmadi. Boshqa nom bilan urinib ko‘ring."
        )
        return

    city_cache[user_id] = {
        city["id"]: city
        for city in cities
    }

    await message.answer(
        "Quyidagi shaharlardan o‘zingiz yashaydiganini tanlang:",
        reply_markup=city_results_keyboard(cities),
    )


@dp.callback_query(F.data.startswith("city:select:"))
async def select_city(callback: CallbackQuery):
    user_id = callback.from_user.id
    city_id = callback.data.split(":")[-1]

    city = city_cache.get(user_id, {}).get(city_id)

    if not city:
        await callback.answer(
            "Shahar ma’lumoti eskirgan. Qayta qidiring.",
            show_alert=True,
        )
        return

    await callback.answer("Shahar tanlandi!")

    await save_city(
        user_id=user_id,
        country=city["country"],
        city=city["name"],
        city_id=city["id"],
        timezone=city["timezone"],
    )

    await callback.message.answer(
        f"📍 Tanlangan shahar: {city['name']}, "
        f"{city['country']}\n\n"
        "Namoz vaqtlaringiz tayyorlanmoqda."
    )

    profile = await get_user(user_id)
    await send_prayer_times(callback.message, profile)


async def send_prayer_times(
    message: Message,
    profile: dict,
):
    try:
        # Open-Meteo shahar qidiruvi natijasidan
        # koordinatalarni qayta olamiz.
        city_results = await search_cities(
            profile["city"]
        )

        city = next(
            (
                item for item in city_results
                if item["id"] == profile["city_id"]
            ),
            None,
        )

        if not city:
            raise ValueError("Shahar koordinatalari topilmadi")

        times = await get_prayer_times(
            latitude=city["latitude"],
            longitude=city["longitude"],
            timezone=profile["timezone"],
        )

        await message.answer(
            format_prayer_times(profile["city"], times),
            reply_markup=prayer_menu(),
        )

        try:
            await message.answer(
                "TAQVO PRO MAX ilovasida Qur’on, zikr, "
                "duolar va boshqa imkoniyatlardan foydalaning.",
                reply_markup=mini_app_keyboard(),
            )
        except RuntimeError:
            logger.warning("MINI_APP_URL hali sozlanmagan")

    except Exception:
        logger.exception("Namoz vaqtlarini yuborishda xatolik")
        await message.answer(
            "Namoz vaqtlarini olishda xatolik yuz berdi. "
            "Keyinroq qayta urinib ko‘ring."
        )


async def main():
    await init_db()

    try:
        await dp.start_polling(bot)
    finally:
        await close_db()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
