"""
TAQVO PRO MAX — SQLite ma'lumotlar bazasi.
Python 3.11+
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Iterator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from config import settings


# =========================================================
# VAQT VA BAZA
# =========================================================

def utc_now() -> str:
    """Joriy UTC vaqtini qaytaradi."""
    return datetime.now(ZoneInfo("UTC")).isoformat(
        timespec="seconds"
    )


def local_today(timezone_name: str | None = None) -> str:
    """Foydalanuvchining mahalliy sanasini qaytaradi."""

    selected_timezone = timezone_name or settings.timezone

    try:
        tz = ZoneInfo(selected_timezone)
    except (ZoneInfoNotFoundError, ValueError):
        tz = ZoneInfo(settings.timezone)

    return datetime.now(tz).date().isoformat()


def _database_path() -> Path:
    """Ma'lumotlar bazasi papkasini tayyorlaydi."""

    path = Path(settings.database_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    return path


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """SQLite bazasiga xavfsiz ulanish."""

    connection = sqlite3.connect(
        str(_database_path()),
        timeout=30,
    )

    connection.row_factory = sqlite3.Row

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")

        yield connection

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def _ensure_user(
    con: sqlite3.Connection,
    user_id: int,
) -> None:
    """Foydalanuvchi mavjudligini tekshiradi."""

    row = con.execute(
        "SELECT user_id FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()

    if row is None:
        raise ValueError(
            "Foydalanuvchi topilmadi. Avval /start yuboring."
        )


def _ensure_user_settings(
    con: sqlite3.Connection,
    user_id: int,
) -> None:
    """Foydalanuvchi sozlamalari mavjudligini kafolatlaydi."""

    now = utc_now()

    con.execute(
        """
        INSERT OR IGNORE INTO user_settings (
            user_id,
            country,
            city,
            timezone,
            prayer_method,
            reminders_enabled,
            morning_reminder,
            evening_reminder,
            updated_at
        )
        VALUES (?, '', '', ?, ?, 0, ?, ?, ?)
        """,
        (
            user_id,
            settings.timezone,
            settings.prayer_method,
            settings.morning_reminder,
            settings.evening_reminder,
            now,
        ),
    )


# =========================================================
# JADVALLARNI YARATISH
# =========================================================

def init_db() -> None:
    """Barcha jadvallar va indekslarni yaratadi."""

    connection = sqlite3.connect(
        str(_database_path()),
        timeout=30,
    )

    try:
        connection.execute("PRAGMA journal_mode = WAL")
    finally:
        connection.close()

    with get_connection() as con:
        con.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT NOT NULL DEFAULT '',
                last_name TEXT NOT NULL DEFAULT '',
                language_code TEXT NOT NULL DEFAULT 'uz',
                is_active INTEGER NOT NULL DEFAULT 1,
                is_subscribed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                country TEXT NOT NULL DEFAULT '',
                city TEXT NOT NULL DEFAULT '',
                timezone TEXT NOT NULL DEFAULT 'Asia/Almaty',
                prayer_method INTEGER NOT NULL DEFAULT 3,
                reminders_enabled INTEGER NOT NULL DEFAULT 0,
                morning_reminder TEXT NOT NULL DEFAULT '08:00',
                evening_reminder TEXT NOT NULL DEFAULT '20:00',
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS tasbeh (
                user_id INTEGER PRIMARY KEY,
                total_count INTEGER NOT NULL DEFAULT 0,
                daily_count INTEGER NOT NULL DEFAULT 0,
                last_date TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quiz_stats (
                user_id INTEGER PRIMARY KEY,
                total_questions INTEGER NOT NULL DEFAULT 0,
                correct_answers INTEGER NOT NULL DEFAULT 0,
                score INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                question_id TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                points INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                reminder_type TEXT NOT NULL,
                message TEXT NOT NULL,
                scheduled_at TEXT NOT NULL,
                sent_at TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_quiz_user
                ON quiz_attempts(user_id);

            CREATE INDEX IF NOT EXISTS idx_reminders_status
                ON reminders(status, scheduled_at);

            CREATE INDEX IF NOT EXISTS idx_reminders_user
                ON reminders(user_id, status);

            CREATE INDEX IF NOT EXISTS idx_users_active
                ON users(is_active);

            CREATE INDEX IF NOT EXISTS idx_users_subscription
                ON users(is_subscribed);
            """
        )


# =========================================================
# FOYDALANUVCHILAR
# =========================================================

def create_user(
    user_id: int,
    first_name: str = "",
    last_name: str = "",
    username: str | None = None,
    language_code: str = "uz",
) -> dict[str, Any]:
    """Foydalanuvchini yaratadi yoki profilini yangilaydi."""

    if user_id <= 0:
        raise ValueError(
            "Telegram user_id musbat bo‘lishi kerak."
        )

    now = utc_now()

    with get_connection() as con:
        con.execute(
            """
            INSERT INTO users (
                user_id,
                username,
                first_name,
                last_name,
                language_code,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)

            ON CONFLICT(user_id) DO UPDATE SET
                username = excluded.username,
                first_name = excluded.first_name,
                last_name = excluded.last_name,
                language_code = excluded.language_code,
                is_active = 1,
                updated_at = excluded.updated_at
            """,
            (
                user_id,
                username,
                first_name or "",
                last_name or "",
                language_code or "uz",
                now,
                now,
            ),
        )

        _ensure_user_settings(con, user_id)

        con.execute(
            """
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                updated_at
            )
            VALUES (?, ?)
            """,
            (user_id, now),
        )

        con.execute(
            """
            INSERT OR IGNORE INTO quiz_stats (
                user_id,
                updated_at
            )
            VALUES (?, ?)
            """,
            (user_id, now),
        )

    result = get_user(user_id)

    if result is None:
        raise RuntimeError(
            "Foydalanuvchi bazaga saqlanmadi."
        )

    return result


def get_user(
    user_id: int,
) -> dict[str, Any] | None:
    """Foydalanuvchi va uning barcha sozlamalarini qaytaradi."""

    with get_connection() as con:
        row = con.execute(
            """
            SELECT
                u.user_id,
                u.username,
                u.first_name,
                u.last_name,
                u.language_code,
                u.is_active,
                u.is_subscribed,
                u.created_at,
                u.updated_at,

                s.country,
                s.city,
                s.timezone,
                s.prayer_method,
                s.reminders_enabled,
                s.morning_reminder,
                s.evening_reminder,

                t.total_count AS tasbeh_total,
                t.daily_count AS tasbeh_daily,

                q.total_questions,
                q.correct_answers,
                q.score

            FROM users AS u

            LEFT JOIN user_settings AS s
                ON s.user_id = u.user_id

            LEFT JOIN tasbeh AS t
                ON t.user_id = u.user_id

            LEFT JOIN quiz_stats AS q
                ON q.user_id = u.user_id

            WHERE u.user_id = ?
            """,
            (user_id,),
        ).fetchone()

    return dict(row) if row else None


def set_subscription(
    user_id: int,
    subscribed: bool,
) -> None:
    """Kanalga obuna holatini saqlaydi."""

    with get_connection() as con:
        cursor = con.execute(
            """
            UPDATE users
            SET is_subscribed = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                int(subscribed),
                utc_now(),
                user_id,
            ),
        )

        if cursor.rowcount == 0:
            raise ValueError("Foydalanuvchi topilmadi.")


# =========================================================
# JOYLASHUV
# =========================================================

def set_location(
    user_id: int,
    country: str,
    city: str,
    timezone_name: str | None = None,
) -> None:
    """Davlat, shahar va vaqt zonasini saqlaydi."""

    country = country.strip()
    city = city.strip()

    if not country or not city:
        raise ValueError(
            "Davlat va shahar nomi bo‘sh bo‘lmasligi kerak."
        )

    selected_timezone = (
        timezone_name or settings.timezone
    ).strip()

    try:
        ZoneInfo(selected_timezone)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(
            f"Vaqt zonasi noto‘g‘ri: {selected_timezone}"
        ) from exc

    now = utc_now()

    with get_connection() as con:
        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        con.execute(
            """
            UPDATE user_settings
            SET country = ?,
                city = ?,
                timezone = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                country,
                city,
                selected_timezone,
                now,
                user_id,
            ),
        )


# =========================================================
# NAMOZ SOZLAMALARI
# =========================================================

def set_prayer_method(
    user_id: int,
    method: int,
) -> None:
    """Namoz hisoblash usulini saqlaydi."""

    if not 0 <= method <= 23:
        raise ValueError(
            "Namoz hisoblash usuli 0–23 oralig‘ida bo‘lishi kerak."
        )

    with get_connection() as con:
        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        con.execute(
            """
            UPDATE user_settings
            SET prayer_method = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                method,
                utc_now(),
                user_id,
            ),
        )


# =========================================================
# ESLATMALAR
# =========================================================

def _validate_reminder_time(value: str) -> str:
    """HH:MM formatini tekshiradi."""

    if not isinstance(value, str):
        raise ValueError(
            "Eslatma vaqti matn bo‘lishi kerak."
        )

    try:
        hour_text, minute_text = value.split(":")
        hour = int(hour_text)
        minute = int(minute_text)
    except (ValueError, AttributeError):
        raise ValueError(
            "Vaqt HH:MM formatida bo‘lishi kerak."
        )

    if not (
        0 <= hour <= 23
        and 0 <= minute <= 59
    ):
        raise ValueError("Eslatma vaqti noto‘g‘ri.")

    return f"{hour:02d}:{minute:02d}"


def set_reminders(
    user_id: int,
    enabled: bool,
    morning: str | None = None,
    evening: str | None = None,
) -> None:
    """Ertalabki va kechki eslatmalar sozlamalarini saqlaydi."""

    morning_time = _validate_reminder_time(
        morning or settings.morning_reminder
    )

    evening_time = _validate_reminder_time(
        evening or settings.evening_reminder
    )

    with get_connection() as con:
        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        con.execute(
            """
            UPDATE user_settings
            SET reminders_enabled = ?,
                morning_reminder = ?,
                evening_reminder = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                int(bool(enabled)),
                morning_time,
                evening_time,
                utc_now(),
                user_id,
            ),
        )


# =========================================================
# TASBEH
# =========================================================

def increment_tasbeh(
    user_id: int,
    amount: int = 1,
) -> dict[str, int]:
    """Tasbeh hisoblagichini oshiradi."""

    if amount <= 0:
        raise ValueError(
            "Miqdor musbat bo‘lishi kerak."
        )

    now = utc_now()

    with get_connection() as con:
        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        profile = con.execute(
            """
            SELECT timezone
            FROM user_settings
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        timezone_name = (
            profile["timezone"] if profile else settings.timezone
        )

        today = local_today(timezone_name)

        row = con.execute(
            """
            SELECT total_count, daily_count, last_date
            FROM tasbeh
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        if row is None:
            con.execute(
                """
                INSERT INTO tasbeh (user_id, updated_at)
                VALUES (?, ?)
                """,
                (user_id, now),
            )

            total = 0
            daily = 0

        else:
            total = row["total_count"]

            daily = (
                row["daily_count"]
                if row["last_date"] == today
                else 0
            )

        total += amount
        daily += amount

        con.execute(
            """
            UPDATE tasbeh
            SET total_count = ?,
                daily_count = ?,
                last_date = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                total,
                daily,
                today,
                now,
                user_id,
            ),
        )

    return {
        "total": total,
        "daily": daily,
    }


def reset_daily_tasbeh(user_id: int) -> None:
    """Kunlik tasbeh hisoblagichini nolga tushiradi."""

    with get_connection() as con:
        _ensure_user(con, user_id)
        _ensure_user_settings(con, user_id)

        profile = con.execute(
            """
            SELECT timezone
            FROM user_settings
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

        timezone_name = (
            profile["timezone"] if profile else settings.timezone
        )

        today = local_today(timezone_name)

        con.execute(
            """
            UPDATE tasbeh
            SET daily_count = 0,
                last_date = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                today,
                utc_now(),
                user_id,
            ),
        )


# =========================================================
# SIYRAT / VIKTORINA NATIJALARI
# =========================================================

def add_quiz_result(
    user_id: int,
    question_id: str,
    is_correct: bool,
    points: int = 20,
) -> dict[str, int]:
    """Viktorina javobi va ballarini saqlaydi."""

    if points < 0:
        raise ValueError(
            "Ball manfiy bo‘lishi mumkin emas."
        )

    if not question_id:
        raise ValueError(
            "Savol ID bo‘sh bo‘lmasligi kerak."
        )

    awarded_points = points if is_correct else 0
    now = utc_now()

    with get_connection() as con:
        _ensure_user(con, user_id)

        con.execute(
            """
            INSERT OR IGNORE INTO quiz_stats (
                user_id,
                updated_at
            )
            VALUES (?, ?)
            """,
            (user_id, now),
        )

        con.execute(
            """
            INSERT INTO quiz_attempts (
                user_id,
                question_id,
                is_correct,
                points,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                str(question_id),
                int(is_correct),
                awarded_points,
                now,
            ),
        )

        con.execute(
            """
            UPDATE quiz_stats
            SET total_questions = total_questions + 1,
                correct_answers = correct_answers + ?,
                score = score + ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                int(is_correct),
                awarded_points,
                now,
                user_id,
            ),
        )

        row = con.execute(
            """
            SELECT
                total_questions,
                correct_answers,
                score
            FROM quiz_stats
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()

    if row is None:
        raise RuntimeError(
            "Viktorina natijasini olish imkoni bo‘lmadi."
        )

    return dict(row)


def get_leaderboard(
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Eng ko‘p ball to‘plagan faol foydalanuvchilar."""

    if not 1 <= limit <= 100:
        raise ValueError(
            "Limit 1 dan 100 gacha bo‘lishi kerak."
        )

    with get_connection() as con:
        rows = con.execute(
            """
            SELECT
                u.first_name,
                q.score,
                q.correct_answers,
                q.total_questions

            FROM quiz_stats AS q

            INNER JOIN users AS u
                ON u.user_id = q.user_id

            WHERE u.is_active = 1

            ORDER BY
                q.score DESC,
                q.correct_answers DESC,
                q.total_questions ASC

            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


# =========================================================
# ESLATMALAR NAVBATI
# =========================================================

def add_reminder(
    user_id: int,
    reminder_type: str,
    message: str,
    scheduled_at: str,
) -> int:
    """Yangi rejalashtirilgan eslatmani bazaga qo‘shadi."""

    if not reminder_type.strip() or not message.strip():
        raise ValueError(
            "Eslatma turi va matni bo‘sh bo‘lmasligi kerak."
        )

    with get_connection() as con:
        _ensure_user(con, user_id)

        cursor = con.execute(
            """
            INSERT INTO reminders (
                user_id,
                reminder_type,
                message,
                scheduled_at,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?, 'pending', ?)
            """,
            (
                user_id,
                reminder_type.strip(),
                message.strip(),
                scheduled_at,
                utc_now(),
            ),
        )

        return int(cursor.lastrowid)


def get_pending_reminders(
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Yuborilishi kutilayotgan eslatmalarni qaytaradi."""

    if not 1 <= limit <= 1000:
        raise ValueError(
            "Limit 1 dan 1000 gacha bo‘lishi kerak."
        )

    with get_connection() as con:
        rows = con.execute(
            """
            SELECT
                r.id,
                r.user_id,
                r.reminder_type,
                r.message,
                r.scheduled_at

            FROM reminders AS r

            INNER JOIN users AS u
                ON u.user_id = r.user_id

            INNER JOIN user_settings AS s
                ON s.user_id = r.user_id

            WHERE r.status = 'pending'
                AND u.is_active = 1
                AND s.reminders_enabled = 1

            ORDER BY r.scheduled_at ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def mark_reminder_sent(reminder_id: int) -> None:
    """Eslatmani yuborilgan deb belgilaydi."""

    with get_connection() as con:
        con.execute(
            """
            UPDATE reminders
            SET status = 'sent',
                sent_at = ?
            WHERE id = ?
                AND status = 'pending'
            """,
            (
                utc_now(),
                reminder_id,
            ),
        )


def mark_reminder_failed(reminder_id: int) -> None:
    """Xatolik bilan yakunlangan eslatmani belgilaydi."""

    with get_connection() as con:
        con.execute(
            """
            UPDATE reminders
            SET status = 'failed'
            WHERE id = ?
                AND status = 'pending'
            """,
            (reminder_id,),
        )


# =========================================================
# FOYDALANUVCHI HOLATI
# =========================================================

def deactivate_user(user_id: int) -> None:
    """Foydalanuvchini faol emas deb belgilaydi."""

    with get_connection() as con:
        con.execute(
            """
            UPDATE users
            SET is_active = 0,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                utc_now(),
                user_id,
            ),
        )


def get_active_user_ids() -> list[int]:
    """Faol foydalanuvchilarning Telegram IDlarini qaytaradi."""

    with get_connection() as con:
        rows = con.execute(
            """
            SELECT user_id
            FROM users
            WHERE is_active = 1
            ORDER BY user_id
            """
        ).fetchall()

    return [
        int(row["user_id"])
        for row in rows
    ]
