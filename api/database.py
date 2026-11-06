"""Asynchronous PostgreSQL database connection."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.config import get_api_settings


settings = get_api_settings()

engine = create_async_engine(
    settings.database_url.get_secret_value(),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=5,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session and close it after use."""

    async with AsyncSessionLocal() as session:
        yield session


async def close_database() -> None:
    """Dispose of the database connection pool."""

    await engine.dispose()
