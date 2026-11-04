import asyncpg

from config import settings


pool: asyncpg.Pool | None = None


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    first_name TEXT NOT NULL DEFAULT '',
    username TEXT,
    language TEXT NOT NULL DEFAULT 'uz-Latn',
    country TEXT,
    city TEXT,
    city_id TEXT,
    timezone TEXT NOT NULL DEFAULT 'UTC',
    calculation_method TEXT NOT NULL DEFAULT 'MWL',
    asr_method TEXT NOT NULL DEFAULT 'Hanafi',
    subscribed BOOLEAN NOT NULL DEFAULT FALSE,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_city
ON users(city_id);

CREATE INDEX IF NOT EXISTS idx_users_enabled
ON users(enabled);
"""


async def init_db() -> None:
    global pool

    if pool is not None:
        return

    pool = await asyncpg.create_pool(
        dsn=settings.DATABASE_URL,
        min_size=1,
        max_size=10,
        command_timeout=30,
    )

    async with pool.acquire() as connection:
        await connection.execute(SCHEMA)


async def close_db() -> None:
    global pool

    if pool is not None:
        await pool.close()
        pool = None


def get_pool() -> asyncpg.Pool:
    if pool is None:
        raise RuntimeError(
            "Database hali ishga tushirilmagan. "
            "Avval init_db() chaqiring."
        )

    return pool


async def save_user(
    user_id: int,
    first_name: str,
    username: str | None = None,
) -> None:
    db = get_pool()

    await db.execute(
        """
        INSERT INTO users (
            id,
            first_name,
            username
        )
        VALUES ($1, $2, $3)
        ON CONFLICT (id)
        DO UPDATE SET
            first_name = EXCLUDED.first_name,
            username = EXCLUDED.username,
            updated_at = NOW()
        """,
        user_id,
        first_name or "",
        username,
    )


async def get_user(user_id: int) -> dict | None:
    db = get_pool()

    row = await db.fetchrow(
        """
        SELECT *
        FROM users
        WHERE id = $1
        """,
        user_id,
    )

    return dict(row) if row else None


async def save_city(
    user_id: int,
    country: str,
    city: str,
    city_id: str,
    timezone: str,
) -> None:
    db = get_pool()

    await db.execute(
        """
        UPDATE users
        SET
            country = $2,
            city = $3,
            city_id = $4,
            timezone = $5,
            updated_at = NOW()
        WHERE id = $1
        """,
        user_id,
        country,
        city,
        city_id,
        timezone,
    )


async def set_subscription(
    user_id: int,
    subscribed: bool,
) -> None:
    db = get_pool()

    await db.execute(
        """
        UPDATE users
        SET
            subscribed = $2,
            updated_at = NOW()
        WHERE id = $1
        """,
        user_id,
        subscribed,
    )


async def set_language(
    user_id: int,
    language: str,
) -> None:
    allowed = {"uz-Latn", "uz-Cyrl"}

    if language not in allowed:
        raise ValueError("Noto‘g‘ri til sozlamasi")

    db = get_pool()

    await db.execute(
        """
        UPDATE users
        SET language = $2,
            updated_at = NOW()
        WHERE id = $1
        """,
        user_id,
        language,
    )


async def get_user_city(
    user_id: int,
) -> dict | None:
    db = get_pool()

    row = await db.fetchrow(
        """
        SELECT country, city, city_id, timezone
        FROM users
        WHERE id = $1
        """,
        user_id,
    )

    return dict(row) if row else None
