"""TAQVO BOT PostgreSQL user management service."""

import logging
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from api.database import AsyncSessionLocal
from api.models import User
from bot.config import get_settings
from bot.services.timezone import is_valid_timezone


logger = logging.getLogger(__name__)


async def get_user_by_telegram_id(
    telegram_id: int,
) -> User | None:
    """Find a user by Telegram ID."""

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(
                User.telegram_id == telegram_id
            )
        )

        return result.scalar_one_or_none()


async def register_or_update_user(
    telegram_id: int,
    first_name: str,
    username: str | None = None,
    language: str = "uz",
) -> User:
    """
    Register a Telegram user or update their profile.

    Existing city, country, and timezone preferences
    are preserved when the user returns.
    """

    if telegram_id <= 0:
        raise ValueError("Telegram ID noto'g'ri.")

    first_name = first_name.strip() or "Foydalanuvchi"

    if len(first_name) > 128:
        first_name = first_name[:128]

    if username:
        username = username.lstrip("@")[:64] or None

    language = language.strip()[:10] or "uz"

    settings = get_settings()
    now = datetime.now(timezone.utc)

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(
                    User.telegram_id == telegram_id
                )
            )

            user = result.scalar_one_or_none()

            if user is None:
                user = User(
                    telegram_id=telegram_id,
                    first_name=first_name,
                    username=username,
                    language=language,
                    timezone=settings.default_timezone,
                    is_active=True,
                    last_seen_at=now,
                )
                session.add(user)

            else:
                user.first_name = first_name
                user.username = username
                user.language = language
                user.last_seen_at = now
                user.is_active = True

            await session.commit()
            await session.refresh(user)

            return user

    except SQLAlchemyError:
        logger.exception(
            "Failed to register Telegram user: %s",
            telegram_id,
        )
        raise


async def update_user_preferences(
    telegram_id: int,
    *,
    language: str | None = None,
    country: str | None = None,
    city: str | None = None,
    timezone_name: str | None = None,
) -> User | None:
    """Update a user's language, city, country and timezone."""

    if language is not None:
        language = language.strip()

        if not language or len(language) > 10:
            raise ValueError("Til kodi noto'g'ri.")

    if country is not None:
        country = country.strip() or None

        if country and len(country) > 100:
            raise ValueError("Davlat nomi juda uzun.")

    if city is not None:
        city = city.strip() or None

        if city and len(city) > 100:
            raise ValueError("Shahar nomi juda uzun.")

    if timezone_name is not None:
        timezone_name = timezone_name.strip()

        if not is_valid_timezone(timezone_name):
            raise ValueError(
                f"Noto'g'ri vaqt mintaqasi: {timezone_name}"
            )

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(
                    User.telegram_id == telegram_id
                )
            )

            user = result.scalar_one_or_none()

            if user is None:
                return None

            if language is not None:
                user.language = language

            if country is not None:
                user.country = country

            if city is not None:
                user.city = city

            if timezone_name is not None:
                user.timezone = timezone_name

            await session.commit()
            await session.refresh(user)

            return user

    except SQLAlchemyError:
        logger.exception(
            "Failed to update user preferences: %s",
            telegram_id,
        )
        raise


async def deactivate_user(
    telegram_id: int,
) -> bool:
    """Deactivate a user without deleting their data."""

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(
                    User.telegram_id == telegram_id
                )
            )

            user = result.scalar_one_or_none()

            if user is None:
                return False

            user.is_active = False

            await session.commit()

            return True

    except SQLAlchemyError:
        logger.exception(
            "Failed to deactivate user: %s",
            telegram_id,
        )
        raise
