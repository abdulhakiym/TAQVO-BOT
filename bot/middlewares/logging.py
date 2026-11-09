
"""TAQVO BOT request logging middleware."""

import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


logger = logging.getLogger("taqvo.middleware")


class LoggingMiddleware(BaseMiddleware):
    """Log incoming updates and unexpected errors."""

    async def __call__(
        self,
        handler: Callable[
            [TelegramObject, dict[str, Any]],
            Awaitable[Any],
        ],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        event_name = type(event).__name__

        logger.info(
            "Incoming Telegram event: %s",
            event_name,
        )

        try:
            result = await handler(event, data)
            return result

        except Exception:
            logger.exception(
                "Error while processing event: %s",
                event_name,
            )
            raise
