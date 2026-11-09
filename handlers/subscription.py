
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ChatMemberStatus

from keyboards import location_keyboard

router = Router()

CHANNEL_USERNAME = "@hakiymqalib"


@router.callback_query(F.data == "subscription:check")
async def check_subscription(callback: CallbackQuery):
    if callback.from_user is None:
        await callback.answer(
            "Foydalanuvchi aniqlanmadi.",
            show_alert=True,
        )
        return

    try:
        member = await callback.bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=callback.from_user.id,
        )

        subscribed = member.status in {
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        }

        if not subscribed:
            await callback.answer(
                "Avval @hakiymqalib kanaliga obuna bo‘ling!",
                show_alert=True,
            )
            return

        await callback.answer("Obuna tasdiqlandi!")

        if callback.message:
            await callback.message.answer(
                "Assalomu alaykum va rohmatullohi va barokatuh! 🤲\n\n"
                "Xush kelibsiz!\n\n"
                "Sizga mos namoz vaqtlarini ko‘rsatishimiz uchun "
                "yashayotgan shahringizni tanlang.",
                reply_markup=location_keyboard(),
            )

    except Exception:
        await callback.answer(
            "Obunani tekshirishda xatolik yuz berdi. "
            "Keyinroq qayta urinib ko‘ring.",
            show_alert=True,
        )
