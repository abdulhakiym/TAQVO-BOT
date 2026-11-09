"""TAQVO BOT application entry point."""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from bot.config import get_settings
from bot.handlers import setup_handlers


def configure_logging(log_level: str) -> None:
    """Configure application logging."""

    level = getattr(
        logging,
        log_level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )


async def main() -> None:
    """Configure and start the Telegram bot."""

    settings = get_settings()

    configure_logging(settings.log_level)

    logger = logging.getLogger(__name__)

    token = settings.bot_token.get_secret_value()

    if not token:
        raise RuntimeError(
            "BOT_TOKEN sozlanmagan. Environment variables "
            "ichida BOT_TOKEN qiymatini kiriting."
        )

    bot = Bot(token=token)
    dispatcher = Dispatcher()

    dispatcher.include_router(setup_handlers())

    logger.info("TAQVO BOT ishga tushmoqda...")

    try:
        await dispatcher.start_polling(bot)

    except Exception:
        logger.exception("TAQVO BOT ishlashida xatolik yuz berdi.")
        raise

    finally:
        await bot.session.close()
        logger.info("TAQVO BOT Telegram sessiyasi yopildi.")


if __name__ == "__main__":
    asyncio.run(main())
