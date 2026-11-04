
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


async def health_check(request: web.Request) -> web.Response:
    """Render server holatini tekshirish uchun endpoint."""
    return web.json_response({
        "status": "ok",
        "service": "TAQVO PRO MAX",
        "bot": "running",
    })


async def start_health_server() -> web.AppRunner:
    """Render uchun HTTP health serverini ishga tushiradi."""
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=settings.port,
    )

    await site.start()

    logger.info(
        "Health server ishga tushdi. Port: %s",
        settings.port,
    )

    return runner


async def main() -> None:
    settings.validate_runtime()

    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logger.info("TAQVO PRO MAX ishga tushmoqda...")

    # Ma'lumotlar bazasini tayyorlash.
    init_db()

    # Telegram bot.
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
        ),
    )

    # Handlerlar uchun umumiy HTTP sessiya.
    http_session = aiohttp.ClientSession()

    # Dispatcher.
    dp = Dispatcher()

    # Barcha handlerlarni ulash.
    dp.include_router(start_router)
    dp.include_router(subscription_router)
    dp.include_router(location_router)
    dp.include_router(prayer_router)
    dp.include_router(settings_router)

    health_runner = None

    try:
        # Render health server.
        health_runner = await start_health_server()

        logger.info("Telegram bot polling boshlandi.")

        await dp.start_polling(
            bot,
            http_session=http_session,
            allowed_updates=dp.resolve_used_update_types(),
        )

    finally:
        logger.info("TAQVO PRO MAX to‘xtatilmoqda...")

        if health_runner is not None:
            await health_runner.cleanup()

        await http_session.close()
        await bot.session.close()

        logger.info("TAQVO PRO MAX to‘xtatildi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot foydalanuvchi tomonidan to‘xtatildi.")
