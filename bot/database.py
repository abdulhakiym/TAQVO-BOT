from __future__ import annotations

import sqlite3
import logging

from contextlib import contextmanager
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Any, Iterator
from zoneinfo import ZoneInfo

from config import settings


logger = logging.getLogger(__name__)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def _database_path() -> Path:
    """SQLite bazasi joylashgan manzil."""

    path = Path(settings.database_path).expanduser()

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def utc_now() -> str:
    """Joriy UTC vaqt."""

    return datetime.now(timezone.utc).isoformat()


def local_today(timezone_name: str | None = None) -> str:
    """Foydalanuvchining mahalliy sanasi."""

    timezone_name = timezone_name or settings.timezone

    try:
        tz = ZoneInfo(timezone_name)
    except Exception:
        tz = ZoneInfo("UTC")

    return datetime.now(tz).date().isoformat()


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """SQLite ulanishini xavfsiz boshqarish."""

    connection = sqlite3.connect(
        str(_database_path()),
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 30000")

    try:
        yield connection
        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def _columns(
    connection: sqlite3.Connection,
    table: str,
) -> set[str]:
    """Jadval ustunlarini olish."""

    rows = connection.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    return {row["name"] for row in rows}


def _add_column(
    connection: sqlite3.Connection,
    table: str,
    column: str,
    definition: str,
) -> None:
    """Eski bazaga yangi ustun qo‘shish."""

    if column not in _columns(connection, table):
        connection.execute(
            f"ALTER TABLE {table} "
            f"ADD COLUMN {column} {definition}"
        )


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db() -> None:
    """Barcha jadvallarni yaratish va bazani yangilash."""

    with get_connection() as con:

        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language_code TEXT DEFAULT 'uz',
                is_subscribed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                city TEXT,
                country TEXT,
                timezone TEXT,
                prayer_method INTEGER NOT NULL DEFAULT 3,
                reminders_enabled INTEGER NOT NULL DEFAULT 1,
                morning_reminder TEXT NOT NULL DEFAULT '08:00',
                evening_reminder TEXT NOT NULL DEFAULT '20:00',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS tasbeh (
                user_id INTEGER PRIMARY KEY,
                total_count INTEGER NOT NULL DEFAULT 0,
                daily_count INTEGER NOT NULL DEFAULT 0,
                last_date TEXT,
                current_zikr TEXT DEFAULT 'Subhanalloh',
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS tasbeh_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                zikr TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS quiz_stats (
                user_id INTEGER PRIMARY KEY,
                total_questions INTEGER NOT NULL DEFAULT 0,
                correct_answers INTEGER NOT NULL DEFAULT 0,
                total_points INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                selected_answer TEXT,
                correct_answer TEXT NOT NULL,
                is_correct INTEGER NOT NULL DEFAULT 0,
                points INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reminder_type TEXT NOT NULL,
                scheduled_at TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                sent_at TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            )
        """)

        # Eski bazalar uchun migratsiya.
        _add_column(
            con, "users", "username", "TEXT"
        )
        _add_column(
            con, "users", "first_name", "TEXT"
        )
        _add_column(
            con, "users", "language_code", "TEXT DEFAULT 'uz'"
        )
        _add_column(
            con, "users", "is_subscribed", "INTEGER NOT NULL DEFAULT 0"
        )
        _add_column(
            con, "users", "created_at", "TEXT"
        )
        _add_column(
            con, "users", "updated_at", "TEXT"
        )

        _add_column(
            con, "user_settings", "city", "TEXT"
        )
        _add_column(
            con, "user_settings", "country", "TEXT"
        )
        _add_column(
            con, "user_settings", "timezone", "TEXT"
        )
        _add_column(
            con, "user_settings", "prayer_method",
            "INTEGER NOT NULL DEFAULT 3"
        )
        _add_column(
            con, "user_settings", "reminders_enabled",
            "INTEGER NOT NULL DEFAULT 1"
        )
        _add_column(
            con, "user_settings", "morning_reminder",
            "TEXT NOT NULL DEFAULT '08:00'"
        )
        _add_column(
            con, "user_settings", "evening_reminder",
            "TEXT NOT NULL DEFAULT '20:00'"
        )
        _add_column(
            con, "user_settings", "created_at", "TEXT"
        )
        _add_column(
            con, "user_settings", "updated_at", "TEXT"
        )

        _add_column(
            con, "tasbeh", "total_count",
            "INTEGER NOT NULL DEFAULT 0"
        )
        _add_column(
            con, "tasbeh", "daily_count",
            "INTEGER NOT NULL DEFAULT 0"
        )
        _add_column(
            con, "tasbeh", "last_date", "TEXT"
        )
        _add_column(
            con, "tasbeh", "current_zikr",
            "TEXT DEFAULT 'Subhanalloh'"
        )
        _add_column(
            con, "tasbeh", "updated_at", "TEXT"
        )

        _add_column(
            con, "quiz_stats", "total_questions",
            "INTEGER NOT NULL DEFAULT 0"
        )
        _add_column(
            con, "quiz_stats", "correct_answers",
            "INTEGER NOT NULL DEFAULT 0"
        )
        _add_column(
            con, "quiz_stats", "total_points",
            "INTEGER NOT NULL DEFAULT 0"
        )
        _add_column(
            con, "quiz_stats", "updated_at", "TEXT"
        )

        _add_column(
            con, "reminders", "reminder_type", "TEXT"
        )
        _add_column(
            con, "reminders", "scheduled_at", "TEXT"
        )
        _add_column(
            con, "reminders", "status",
            "TEXT NOT NULL DEFAULT 'pending'"
        )
        _add_column(
            con, "reminders", "sent_at", "TEXT"
        )
        _add_column(
            con, "reminders", "created_at", "TEXT"
        )

        now = utc_now()

        con.execute("""
            UPDATE users
            SET created_at = COALESCE(created_at, ?),
                updated_at = COALESCE(updated_at, ?)
        """, (now, now))

        con.execute("""
            UPDATE user_settings
            SET created_at = COALESCE(created_at, ?),
                updated_at = COALESCE(updated_at, ?)
        """, (now, now))

        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_reminders_due
            ON reminders(status, scheduled_at)
        """)

        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_quiz_user
            ON quiz_attempts(user_id, created_at)
        """)

        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasbeh_user
            ON tasbeh_history(user_id, created_at)
        """)

    logger.info("TAQVO PRO MAX database initialized.")


# =========================================================
# USER MANAGEMENT
# =========================================================

def _ensure_user(
    con: sqlite3.Connection,
    user_id: int,
) -> None:

    now = utc_now()

    con.execute("""
        INSERT OR IGNORE INTO users (
            user_id,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?)
    """, (user_id, now, now))


def _ensure_user_settings(
    con: sqlite3.Connection,
    user_id: int,
) -> None:

    now = utc_now()

    con.execute("""
        INSERT OR IGNORE INTO user_settings (
            user_id,
            timezone,
            prayer_method,
            reminders_enabled,
            morning_reminder,
            evening_reminder,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, 1, ?, ?, ?, ?)
    """, (
        user_id,
        settings.timezone,
        settings.prayer_method,
        settings.morning_reminder,
        settings.evening_reminder,
        now,
        now,
    ))


def create_user(
    user_id: int,
    username: str | None = None,
    first_name: str | None = None,
    language_code: str = "uz",
) -> None:

    now = utc_now()

    with get_connection() as con:

        con.execute("""
            INSERT INTO users (
                user_id,
                username,
                first_name,
                language_code,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                language_code = excluded.language_code,
                updated_at = excluded.updated_at
        """, (
            user_id,
            username,
            first_name,
            language_code,
            now,
            now,
        ))

        _ensure_user_settings(con, user_id)

        con.execute("""
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, now))

        con.execute("""
            INSERT OR IGNORE INTO quiz_stats (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, now))


def get_user(user_id: int) -> dict[str, Any] | None:

    with get_connection() as con:

        row = con.execute("""
            SELECT
                u.user_id,
                u.username,
                u.first_name,
                u.language_code,
                u.is_subscribed,
                s.city,
                s.country,
                s.timezone,
                s.prayer_method,
                s.reminders_enabled,
                s.morning_reminder,
                s.evening_reminder
            FROM users u
            LEFT JOIN user_settings s
                ON s.user_id = u.user_id
            WHERE u.user_id = ?
        """, (user_id,)).fetchone()

        return dict(row) if row else None


def set_subscription(
    user_id: int,
    subscribed: bool,
) -> None:

    with get_connection() as con:

        _ensure_user(con, user_id)

        con.execute("""
            UPDATE users
            SET is_subscribed = ?,
                updated_at = ?
            WHERE user_id = ?
        """, (int(subscribed), utc_now(), user_id))


def is_subscribed(user_id: int) -> bool:

    user = get_user(user_id)

    return bool(user and user["is_subscribed"])


# =========================================================
# USER SETTINGS
# =========================================================

def set_location(
    user_id: int,
    country: str,
    city: str,
    timezone_name: str | None = None,
) -> None:

    with get_connection() as con:

        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        con.execute("""
            UPDATE user_settings
            SET country = ?,
                city = ?,
                timezone = COALESCE(?, timezone),
                updated_at = ?
            WHERE user_id = ?
        """, (
            country,
            city,
            timezone_name,
            utc_now(),
            user_id,
        ))


def set_prayer_method(
    user_id: int,
    method: int,
) -> None:

    if not 0 <= int(method) <= 23:
        raise ValueError("Namoz hisoblash usuli noto‘g‘ri.")

    with get_connection() as con:

        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        con.execute("""
            UPDATE user_settings
            SET prayer_method = ?,
                updated_at = ?
            WHERE user_id = ?
        """, (int(method), utc_now(), user_id))


def set_reminders(
    user_id: int,
    enabled: bool,
    morning: str | None = None,
    evening: str | None = None,
) -> None:

    with get_connection() as con:

        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        con.execute("""
            UPDATE user_settings
            SET reminders_enabled = ?,
                morning_reminder = COALESCE(?, morning_reminder),
                evening_reminder = COALESCE(?, evening_reminder),
                updated_at = ?
            WHERE user_id = ?
        """, (
            int(enabled),
            morning,
            evening,
            utc_now(),
            user_id,
        ))


# =========================================================
# TASBEH
# =========================================================

def get_tasbeh(user_id: int) -> dict[str, Any]:

    today = local_today()

    with get_connection() as con:

        _ensure_user(con, user_id)

        con.execute("""
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, utc_now()))

        row = con.execute("""
            SELECT *
            FROM tasbeh
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        if row["last_date"] != today:
            con.execute("""
                UPDATE tasbeh
                SET daily_count = 0,
                    last_date = ?,
                    updated_at = ?
                WHERE user_id = ?
            """, (today, utc_now(), user_id))

            row = con.execute("""
                SELECT *
                FROM tasbeh
                WHERE user_id = ?
            """, (user_id,)).fetchone()

        return dict(row)


def add_tasbeh(
    user_id: int,
    zikr: str = "Subhanalloh",
    count: int = 1,
) -> dict[str, Any]:

    if count < 1 or count > 1000:
        raise ValueError("Tasbeh soni noto‘g‘ri.")

    today = local_today()
    now = utc_now()

    with get_connection() as con:

        _ensure_user(con, user_id)

        con.execute("""
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                last_date,
                updated_at
            )
            VALUES (?, ?, ?)
        """, (user_id, today, now))

        con.execute("""
            UPDATE tasbeh
            SET
                daily_count = CASE
                    WHEN last_date = ? THEN daily_count + ?
                    ELSE ?
                END,
                total_count = total_count + ?,
                last_date = ?,
                current_zikr = ?,
                updated_at = ?
            WHERE user_id = ?
        """, (
            today,
            count,
            count,
            count,
            today,
            zikr,
            now,
            user_id,
        ))

        con.execute("""
            INSERT INTO tasbeh_history (
                user_id,
                zikr,
                count,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (user_id, zikr, count, now))

    return get_tasbeh(user_id)


def reset_daily_tasbeh(user_id: int) -> None:

    with get_connection() as con:

        _ensure_user(con, user_id)

        con.execute("""
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, utc_now()))

        con.execute("""
            UPDATE tasbeh
            SET daily_count = 0,
                last_date = ?,
                updated_at = ?
            WHERE user_id = ?
        """, (local_today(), utc_now(), user_id))


def set_current_zikr(
    user_id: int,
    zikr: str,
) -> None:

    with get_connection() as con:

        _ensure_user(con)

        con.execute("""
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, utc_now()))

        con.execute("""
            UPDATE tasbeh
            SET current_zikr = ?,
                updated_at = ?
            WHERE user_id = ?
        """, (zikr, utc_now(), user_id))


def get_tasbeh_history(
    user_id: int,
    limit: int = 20,
) -> list[dict[str, Any]]:

    limit = max(1, min(int(limit), 100))

    with get_connection() as con:

        rows = con.execute("""
            SELECT zikr, SUM(count) AS count
            FROM tasbeh_history
            WHERE user_id = ?
            GROUP BY zikr
            ORDER BY count DESC
            LIMIT ?
        """, (user_id, limit)).fetchall()

        return [dict(row) for row in rows]


# =========================================================
# QUIZ / VIKTORINA
# =========================================================

def get_quiz_stats(user_id: int) -> dict[str, Any]:

    with get_connection() as con:

        _ensure_user(con, user_id)

        con.execute("""
            INSERT OR IGNORE INTO quiz_stats (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, utc_now()))

        row = con.execute("""
            SELECT *
            FROM quiz_stats
            WHERE user_id = ?
        """, (user_id,)).fetchone()

        return dict(row)


def record_quiz_answer(
    user_id: int,
    question: str,
    selected_answer: str,
    correct_answer: str,
    points: int = 20,
) -> dict[str, Any]:

    if points < 0 or points > 1000:
        raise ValueError("Viktorina ballari noto‘g‘ri.")

    is_correct = (
        selected_answer.strip().casefold()
        == correct_answer.strip().casefold()
    )

    earned_points = points if is_correct else 0
    now = utc_now()

    with get_connection() as con:

        _ensure_user(con, user_id)

        con.execute("""
            INSERT OR IGNORE INTO quiz_stats (
                user_id,
                updated_at
            )
            VALUES (?, ?)
        """, (user_id, now))

        con.execute("""
            INSERT INTO quiz_attempts (
                user_id,
                question,
                selected_answer,
                correct_answer,
                is_correct,
                points,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            question,
            selected_answer,
            correct_answer,
            int(is_correct),
            earned_points,
            now,
        ))

        con.execute("""
            UPDATE quiz_stats
            SET
                total_questions = total_questions + 1,
                correct_answers = correct_answers + ?,
                total_points = total_points + ?,
                updated_at = ?
            WHERE user_id = ?
        """, (
            int(is_correct),
            earned_points,
            now,
            user_id,
        ))

    return get_quiz_stats(user_id)


def get_quiz_leaderboard(
    limit: int = 10,
) -> list[dict[str, Any]]:

    limit = max(1, min(int(limit), 100))

    with get_connection() as con:

        rows = con.execute("""
            SELECT
                u.user_id,
                COALESCE(u.first_name, 'Foydalanuvchi') AS name,
                q.total_points,
                q.correct_answers,
                q.total_questions
            FROM quiz_stats q
            JOIN users u ON u.user_id = q.user_id
            ORDER BY
                q.total_points DESC,
                q.correct_answers DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]


# =========================================================
# REMINDERS
# =========================================================

def add_reminder(
    user_id: int,
    reminder_type: str,
    scheduled_at: str,
) -> int:

    if reminder_type not in {
        "morning",
        "evening",
        "custom",
    }:
        raise ValueError("Eslatma turi noto‘g‘ri.")

    with get_connection() as con:

        _ensure_user(con, user_id)

        cursor = con.execute("""
            INSERT INTO reminders (
                user_id,
                reminder_type,
                scheduled_at,
                status,
                created_at
            )
            VALUES (?, ?, ?, 'pending', ?)
        """, (
            user_id,
            reminder_type,
            scheduled_at,
            utc_now(),
        ))

        return int(cursor.lastrowid)


def get_pending_reminders(
    before: str | None = None,
    limit: int = 500,
) -> list[dict[str, Any]]:

    before = before or utc_now()
    limit = max(1, min(int(limit), 2000))

    with get_connection() as con:

        rows = con.execute("""
            SELECT *
            FROM reminders
            WHERE status = 'pending'
              AND scheduled_at <= ?
            ORDER BY scheduled_at ASC
            LIMIT ?
        """, (before, limit)).fetchall()

        return [dict(row) for row in rows]


def mark_reminder_sent(reminder_id: int) -> None:

    with get_connection() as con:

        con.execute("""
            UPDATE reminders
            SET status = 'sent',
                sent_at = ?
            WHERE id = ?
        """, (utc_now(), reminder_id))


def mark_reminder_failed(reminder_id: int) -> None:

    with get_connection() as con:

        con.execute("""
            UPDATE reminders
            SET status = 'failed'
            WHERE id = ?
        """, (reminder_id,))


def get_active_users() -> list[dict[str, Any]]:

    with get_connection() as con:

        rows = con.execute("""
            SELECT
                u.user_id,
                s.city,
                s.country,
                s.timezone,
                s.reminders_enabled,
                s.morning_reminder,
                s.evening_reminder
            FROM users u
            JOIN user_settings s
                ON s.user_id = u.user_id
            WHERE u.is_subscribed = 1
        """).fetchall()

        return [dict(row) for row in rows]


def get_reminder_users() -> list[dict[str, Any]]:

    with get_connection() as con:

        rows = con.execute("""
            SELECT
                u.user_id,
                s.city,
                s.country,
                s.timezone,
                s.morning_reminder,
                s.evening_reminder
            FROM users u
            JOIN user_settings s
                ON s.user_id = u.user_id
            WHERE u.is_subscribed = 1
              AND s.reminders_enabled = 1
        """).fetchall()

        return [dict(row) for row in rows]


# =========================================================
# DATABASE HEALTH
# =========================================================

def database_health() -> dict[str, Any]:

    with get_connection() as con:

        result = con.execute(
            "PRAGMA quick_check"
        ).fetchone()

        user_count = con.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]

        return {
            "status": result[0],
            "users": user_count,
            "database": str(_database_path()),
        }
