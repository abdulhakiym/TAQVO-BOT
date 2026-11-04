
from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramNetworkError
from aiogram.types import ChatMember

from config import settings


logger = logging.getLogger(__name__)


async def check_subscription(
    bot: Bot,
    user_id: int,
) -> bool:
    """
    Foydalanuvchining @hakiymqalb kanaliga obunasini tekshiradi.

    True  — obuna bo‘lgan.
    False — obuna bo‘lmagan yoki tekshiruvda xatolik yuz bergan.
    """

    try:
        member: ChatMember = await bot.get_chat_member(
            chat_id=settings.channel_username,
            user_id=user_id,
        )

        if member.status in ("creator", "administrator", "member"):
            return True

        if member.status == "restricted":
            return bool(member.is_member)

        return False

    except TelegramBadRequest as error:
        logger.warning(
            "Obunani tekshirishda Telegram xatoligi. "
            "User ID: %s. Xatolik: %s",
            user_id,
            error,
        )
        return False

    except TelegramNetworkError:
        logger.exception(
            "Telegram serveriga ulanishda xatolik. User ID: %s",
            user_id,
        )
        return False

    except Exception:
        logger.exception(
            "Obunani tekshirishda kutilmagan xatolik. User ID: %s",
            user_id,
        )
        return False
