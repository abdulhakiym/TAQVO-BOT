import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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
    city_results_keyboard,
    mini_app_keyboard,
)

from prayer_times import (
    search_cities,
    get_prayer_times,
    format_prayer_times,
)


# ==================================================
# LOGGING
# ==================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("TAQVO_PRO_MAX")


# ==================================================
# BOT VA DISPATCHER
# ==================================================

bot = Bot(token=settings.BOT_TOKEN)

dp = Dispatcher(storage=MemoryStorage())


# ==================================================
# FOYDALANUVCHI HOLATLARI
# ==================================================

class CitySearch(StatesGroup):
    waiting_city = State()


# ==================================================
# PASTKI MENYU
# ==================================================

def prayer_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🕌 Namoz vaqtlarim"
                )
            ]
        ],
        resize_keyboard=True,
        is_persistent=True,
    )


# ==================================================
# OBUNANI TEKSHIRISH
# ==================================================

async def check_subscription(user_id: int) -> bool:
    member = await bot.get_chat_member(
        chat_id=settings.CHANNEL_USERNAME,
        user_id=user_id,
    )

    return member.status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
    }


async def ask_subscription(message: Message) -> None:
    await message.answer(
        "🤲 TAQVO PRO MAX xizmatidan foydalanish uchun "
        "avval rasmiy kanalimizga obuna bo‘ling.\n\n"
        "1. Kanalga obuna bo‘ling.\n"
        "2. «Obunani tasdiqlash» tugmasini bosing.\n\n"
        "Bot obunangizni tekshiradi.",
        reply_markup=subscription_keyboard(),
    )


# ==================================================
# SHAXSIY SALOMLASHUV
# ==================================================

async def welcome_user(message: Message) -> None:
    user = message.from_user

    name = (
        user.first_name.strip()
        if user and user.first_name
        else "aziz birodar"
    )

    await message.answer(
        "Assalomu alaykum va rohmatullohi va barokatuh! 🤲\n\n"
        f"Xush kelibsiz, {name}!\n\n"
        "TAQVO PRO MAX loyihasiga xush kelibsiz.\n"
        "Alloh ilmingizga va amallaringizga baraka bersin."
    )

    await message.answer(
        "🌍 Yashayotgan davlatingizni tanlang:",
        reply_markup=country_keyboard(),
    )


# ==================================================
# MINI APP TAKLIFI
# ==================================================

async def send_mini_app(message: Message) -> None:
    text = (
        "🌙 TAQVO PRO MAX sizni kutmoqda!\n\n"
        "Qur’oni Karim, sahih hadislar, zikrlar, duolar, "
        "TAQVO AI va boshqa imkoniyatlardan foydalaning."
    )

    try:
        keyboard = mini_app_keyboard()

        await message.answer(
            text,
            reply_markup=keyboard,
        )

    except (RuntimeError, ValueError):
        logger.exception("Mini App tugmasini yaratishda xatolik")

        await message.answer(
            text + "\n\nIlova manzili hozircha sozlanmagan."
        )


# ==================================================
# NAMOZ VAQTLARINI YUBORISH
# ==================================================

async def send_prayer_times(
    message: Message,
    profile: dict,
) -> None:

    if not profile:
        await message.answer(
            "Foydalanuvchi ma’lumotlari topilmadi. "
            "/start buyrug‘ini bosing."
        )
        return

    city_name = profile.get("city")
    city_id = profile.get("city_id")
    timezone = profile.get("timezone")

    if not city_name or not city_id or not timezone:
        await message.answer(
            "Shahar ma’lumotlari to‘liq emas. "
            "Iltimos, shahringizni qayta tanlang."
        )
        return

    try:
        cities = await search_cities(city_name)

        city = next(
            (
                item for item in cities
                if str(item["id"]) == str(city_id)
            ),
            None,
        )

        if city is None:
            city = next(
                (
                    item for item in cities
                    if item["name"].casefold()
                    == city_name.casefold()
                ),
                None,
            )

        if city is None:
            raise ValueError(
                "Shahar koordinatalari topilmadi."
            )

        times = await get_prayer_times(
            latitude=city["latitude"],
            longitude=city["longitude"],
            timezone=timezone,
        )

        await message.answer(
            format_prayer_times(city_name, times),
            reply_markup=prayer_menu(),
        )

        await send_mini_app(message)

    except Exception:
        logger.exception(
            "Namoz vaqtlarini olishda xatolik: user=%s",
            message.from_user.id,
        )

        await message.answer(
            "Namoz vaqtlarini olishda xatolik yuz berdi.\n"
            "Internet aloqasini tekshirib, keyinroq urinib ko‘ring.",
            reply_markup=prayer_menu(),
        )


# ==================================================
# /START
# ==================================================

@dp.message(CommandStart())
async def start(
    message: Message,
    state: FSMContext,
):
    user = message.from_user

    await state.clear()

    await save_user(
        user_id=user.id,
        first_name=user.first_name or "",
        username=user.username,
    )

    try:
        subscribed = await check_subscription(user.id)

    except TelegramAPIError:
        logger.exception("Obunani tekshirishda Telegram xatosi")

        await message.answer(
            "Kanal obunasini tekshirish vaqtincha imkonsiz.\n"
            "Birozdan keyin qayta urinib ko‘ring."
        )
        return

    if not subscribed:
        await set_subscription(user.id, False)
        await ask_subscription(message)
        return

    await set_subscription(user.id, True)

    profile = await get_user(user.id)

    if profile and profile.get("city"):
        await message.answer(
            f"Assalomu alaykum va rohmatullohi va barokatuh, "
            f"{user.first_name or 'aziz birodar'}! 🤲"
        )

        await send_prayer_times(message, profile)
        return

    await welcome_user(message)


# ==================================================
# OBUNANI TASDIQLASH
# ==================================================

@dp.callback_query(F.data == "subscription:check")
async def verify_subscription(
    callback: CallbackQuery,
    state: FSMContext,
):
    user = callback.from_user

    try:
        subscribed = await check_subscription(user.id)

    except TelegramAPIError:
        logger.exception("Obuna qayta tekshirilishida xatolik")

        await callback.answer(
            "Tekshirish imkoni bo‘lmadi. Keyinroq urinib ko‘ring.",
            show_alert=True,
        )
        return

    if not subscribed:
        await callback.answer(
            "Siz hali kanalga obuna bo‘lmagansiz.",
            show_alert=True,
        )
        return

    await set_subscription(user.id, True)

    await save_user(
        user_id=user.id,
        first_name=user.first_name or "",
        username=user.username,
    )

    await callback.answer("Obuna tasdiqlandi!")

    await state.clear()

    try:
        await callback.message.delete()
    except TelegramAPIError:
        pass

    await callback.bot.send_message(
        user.id,
        "Assalomu alaykum va rohmatullohi va barokatuh! 🤲\n\n"
        f"Xush kelibsiz, {user.first_name or 'aziz birodar'}!\n\n"
        "🌍 Yashayotgan davlatingizni tanlang:",
        reply_markup=country_keyboard(),
    )


# ==================================================
# DAVLAT TANLASH
# ==================================================

@dp.callback_query(F.data.startswith("country:"))
async def choose_country(
    callback: CallbackQuery,
    state: FSMContext,
):
    country_code = callback.data.split(":", 1)[1]

    await callback.answer()

    if country_code == "other":
        country_code = ""

    await state.clear()

    await state.set_state(CitySearch.waiting_city)

    await state.update_data(
        country_code=country_code,
    )

    await callback.message.answer(
        "🔎 Endi yashayotgan shahringiz nomini yozing.\n\n"
        "Masalan: Toshkent, Olmaota, Moskva, Madina."
    )


# ==================================================
# SHAHAR QIDIRISH
# ==================================================

@dp.message(CitySearch.waiting_city, F.text)
async def search_city_handler(
    message: Message,
    state: FSMContext,
):
    query = message.text.strip()

    if len(query) < 2:
        await message.answer(
            "Shahar nomini kamida 2 ta harf bilan kiriting."
        )
        return

    data = await state.get_data()

    country_code = data.get("country_code", "")

    try:
        cities = await search_cities(query)

    except Exception:
        logger.exception("Shahar qidirishda xatolik")

        await message.answer(
            "Shaharlarni qidirish xizmati ishlamayapti. "
            "Keyinroq qayta urinib ko‘ring."
        )
        return

    if country_code:
        cities = [
            city for city in cities
            if city.get("country_code", "").upper()
            == country_code.upper()
        ]

    if not cities:
        await message.answer(
            "Shahar topilmadi.\n"
            "Nomini tekshiring yoki boshqa nom bilan qidiring."
        )
        return

    # Callback ma'lumotlari va FSM ichidagi natijalar mos saqlanadi.
    await state.update_data(
        city_results=cities,
    )

    await message.answer(
        "📍 Quyidagi shaharlardan birini tanlang:",
        reply_markup=city_results_keyboard(cities),
    )


# ==================================================
# SHAHARNI TANLASH
# ==================================================

@dp.callback_query(F.data.startswith("city:select:"))
async def select_city(
    callback: CallbackQuery,
    state: FSMContext,
):
    user_id = callback.from_user.id

    city_id = callback.data.split(":", 2)[2]

    data = await state.get_data()

    cities = data.get("city_results", [])

    city = next(
        (
            item for item in cities
            if str(item.get("id")) == city_id
        ),
        None,
    )

    if city is None:
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
        city_id=str(city["id"]),
        timezone=city["timezone"],
    )

    await state.clear()

    try:
        await callback.message.delete()
    except TelegramAPIError:
        pass

    await callback.bot.send_message(
        user_id,
        f"📍 Tanlangan shahar: {city['name']}, "
        f"{city['country']}\n\n"
        "Namoz vaqtlaringiz hisoblanmoqda...",
    )

    profile = await get_user(user_id)

    if profile:
        await send_prayer_times(
            callback.message,
            profile,
        )


# ==================================================
# NAMOZ VAQTLARI TUGMASI
# ==================================================

@dp.message(F.text == "🕌 Namoz vaqtlarim")
async def prayer_button(message: Message):
    profile = await get_user(message.from_user.id)

    if not profile or not profile.get("city"):
        await message.answer(
            "Avval davlatingiz va shahringizni tanlang."
        )
        await welcome_user(message)
        return

    await send_prayer_times(message, profile)


# ==================================================
# SHAHAR TANLOVINI QAYTA BOSHLASH
# ==================================================

@dp.message(F.text == "🌍 Shaharni o‘zgartirish")
async def change_city(
    message: Message,
    state: FSMContext,
):
    await state.clear()

    await message.answer(
        "🌍 Davlatingizni tanlang:",
        reply_markup=country_keyboard(),
    )


# ==================================================
# BOTNI ISHGA TUSHIRISH
# ==================================================

async def main():
    logger.info("TAQVO PRO MAX ishga tushmoqda...")

    await init_db()

    try:
        await bot.delete_webhook(drop_pending_updates=True)

        logger.info("Telegram polling boshlandi.")

        await dp.start_polling(bot)

    finally:
        await close_db()
        await bot.session.close()

        logger.info("TAQVO PRO MAX to‘xtatildi.")


if __name__ == "__main__":
    asyncio.run(main())
