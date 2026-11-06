"""TAQVO BOT message and callback handlers."""

from aiogram import Router

from bot.handlers.start import router as start_router


def setup_handlers() -> Router:
    """Create the main router and register all handlers."""

    main_router = Router(name="main")

    main_router.include_router(start_router)

    return main_router
