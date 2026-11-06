"""TAQVO BOT application entry point."""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import get_settings
from bot.handlers import setup_handlers


async def main() -> None:
    """Configure and start the Telegram bot."""

    settings = get_settings()

    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )

    bot = Bot(
        token=settings.bot_token.get_secret_value()
    )

    dispatcher = Dispatcher()
    dispatcher.include_router(setup_handlers())

    logging.info("TAQVO BOT ishga tushmoqda...")

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
