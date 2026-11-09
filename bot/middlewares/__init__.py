
"""TAQVO BOT message and callback handlers."""

from aiogram import Router

from bot.handlers.start import router as start_router
from bot.middlewares import LoggingMiddleware


def setup_handlers() -> Router:
    """Create the main router and register handlers."""

    main_router = Router(name="main")

    # Register request logging middleware.
    main_router.message.outer_middleware(
        LoggingMiddleware()
    )

    main_router.callback_query.outer_middleware(
        LoggingMiddleware()
    )

    # Register feature routers.
    main_router.include_router(start_router)

    return main_router
