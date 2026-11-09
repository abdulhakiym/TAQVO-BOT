"""TAQVO BOT message and callback handlers."""

from aiogram import Router

from bot.handlers.start import router as start_router
from bot.middlewares import LoggingMiddleware


def setup_handlers() -> Router:
    """Create the main router and register all handlers."""

    main_router = Router(name="main")

    # Register logging middleware for incoming updates.
    main_router.message.outer_middleware(
        LoggingMiddleware()
    )

    main_router.callback_query.outer_middleware(
        LoggingMiddleware()
    )

    # Register application handlers.
    main_router.include_router(start_router)

    return main_router
