from __future__ import annotations

import asyncio
import logging

import aiohttp
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import settings
from database import init_db

from handlers.start import router as start_router
from handlers.subscription import router as subscription_router
from handlers.location import router as location_router
from handlers.prayer import router as prayer_router
from handlers.settings import router as settings_router


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Log yozuvlarini sozlaydi."""

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)s | "
            "%(name)s | %(message)s"
        ),
    )


async def health_check(request: web.Request) -> web.Response:
    """Render server holatini tekshirish endpointi."""

    return web.json_response({
        "status": "ok",
        "service": "TAQVO PRO MAX",
        "bot": "running",
    })


async def start_health_server() -> web.AppRunner:
    """HTTP health serverini ishga tushiradi."""

    app = web.Application()

    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()

    try:
        site = web.TCPSite(
            runner,
            host="0.0.0.0",
            port=settings.port,
        )

        await site.start()

    except Exception:
        await runner.cleanup()
        raise

    logger.info(
        "Health server ishga tushdi. Port: %s",
        settings.port,
    )

    return runner


def register_routers(dp: Dispatcher) -> None:
    """Barcha Telegram handlerlarini ulaydi."""

    dp.include_router(start_router)
    dp.include_router(subscription_router)
    dp.include_router(location_router)
    dp.include_router(prayer_router)
    dp.include_router(settings_router)


async def main() -> None:
    configure_logging()

    logger.info("TAQVO PRO MAX ishga tushmoqda...")

    # Muhit sozlamalarini tekshirish.
    settings.validate_runtime()

    # Ma'lumotlar bazasini tayyorlash.
    init_db()

    # Telegram botni yaratish.
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    # Dispatcher.
    dp = Dispatcher()

    register_routers(dp)

    health_runner: web.AppRunner | None = None

    # HTTP so'rovlar uchun timeout.
    timeout = aiohttp.ClientTimeout(
        total=settings.http_timeout_seconds,
    )

    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
        ) as http_session:

            # Handlerlarga umumiy HTTP sessiyani uzatish.
            health_runner = await start_health_server()

            logger.info("Telegram bot polling boshlandi.")

            await dp.start_polling(
                bot,
                http_session=http_session,
                allowed_updates=dp.resolve_used_update_types(),
                close_bot_session=False,
            )

    finally:
        logger.info("TAQVO PRO MAX to‘xtatilmoqda...")

        if health_runner is not None:
            await health_runner.cleanup()

        await bot.session.close()

        logger.info("TAQVO PRO MAX to‘xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        logging.getLogger(__name__).info(
            "Bot foydalanuvchi tomonidan to‘xtatildi."
        )

    except Exception:
        logging.getLogger(__name__).exception(
            "TAQVO PRO MAX ishga tushishida jiddiy xatolik."
        )
        raise
