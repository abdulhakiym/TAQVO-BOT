"""Alembic migration environment for TAQVO."""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from api.config import get_api_settings
from api.models import Base, User  # noqa: F401


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_api_settings()
database_url = settings.database_url.get_secret_value()

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""

    config.set_main_option(
        "sqlalchemy.url",
        database_url.replace("%", "%%"),
    )

    context.configure(
        url=database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    """Configure and execute migrations using a live connection."""

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async connection and run migrations."""

    connectable = create_async_engine(
        database_url,
        poolclass=pool.NullPool,
    )

    try:
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations with an asynchronous database connection."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
