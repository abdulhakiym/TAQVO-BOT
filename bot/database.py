"""
TAQVO PRO MAX — SQLite ma'lumotlar bazasi.
Python 3.11+
Xavfsiz ulanish, migratsiya va ma'lumotlarni boshqarish.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, time
from pathlib import Path
from typing import Any, Iterator
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from config import settings


# =========================================================
# UMUMIY SOZLAMALAR
# =========================================================

def utc_now() -> str:
    """Joriy UTC vaqtini ISO formatida qaytaradi."""
    return datetime.now(ZoneInfo("UTC")).isoformat(
        timespec="seconds"
    )


def local_today(timezone_name: str | None = None) -> str:
    """Foydalanuvchining mahalliy sanasini qaytaradi."""

    selected_timezone = timezone_name or settings.timezone

    try:
        timezone = ZoneInfo(selected_timezone)
    except (ZoneInfoNotFoundError, ValueError):
        timezone = ZoneInfo(settings.timezone)

    return datetime.now(timezone).date().isoformat()


def _database_path() -> Path:
    """Baza fayli joylashadigan papkani tayyorlaydi."""

    path = Path(settings.database_path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)

    return path


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """SQLite bazasiga xavfsiz ulanish va tranzaksiya."""

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


def _validate_user_id(user_id: int) -> None:
    if isinstance(user_id, bool) or not isinstance(user_id, int):
        raise ValueError("Telegram user_id butun son bo‘lishi kerak.")

    if user_id <= 0:
        raise ValueError("Telegram user_id musbat bo‘lishi kerak.")


def _validate_timezone(timezone_name: str) -> str:
    if not isinstance(timezone_name, str) or not timezone_name.strip():
        raise ValueError("Vaqt zonasi ko‘rsatilmagan.")

    timezone_name = timezone_name.strip()

    try:
        ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(
            f"Vaqt zonasi noto‘g‘ri: {timezone_name}"
        ) from exc

    return timezone_name


def _validate_prayer_method(method: int) -> int:
    if isinstance(method, bool) or not isinstance(method, int):
        raise ValueError("Hisoblash usuli butun son bo‘lishi kerak.")

    if not 0 <= method <= 23:
        raise ValueError(
            "Namoz hisoblash usuli 0–23 oralig‘ida bo‘lishi kerak."
        )

    return method


def _validate_reminder_time(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Eslatma vaqti matn bo‘lishi kerak.")

    try:
        parsed = time.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValueError(
            "Eslatma vaqti HH:MM formatida bo‘lishi kerak."
        ) from exc

    if parsed.tzinfo is not None or parsed.second or parsed.microsecond:
        raise ValueError("Eslatma vaqti HH:MM formatida bo‘lishi kerak.")

    return parsed.strftime("%H:%M")


def _validate_scheduled_at(value: str) -> str:
    """Eslatma sanasini ISO 8601 formatida tekshiradi."""

    if not isinstance(value, str) or not value.strip():
        raise ValueError("Eslatma sanasi ko‘rsatilmagan.")

    value = value.strip()

    try:
        parsed = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError(
            "Sana ISO 8601 formatida bo‘lishi kerak."
        ) from exc

    if parsed.tzinfo is None:
        raise ValueError(
            "Eslatma sanasida vaqt zonasi ko‘rsatilishi kerak."
        )

    return parsed.isoformat(timespec="seconds")


def _ensure_user(
    con: sqlite3.Connection,
    user_id: int,
) -> None:
    _validate_user_id(user_id)

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
# BAZA MIGRATSIYASI
# =========================================================

def _add_missing_columns(
    con: sqlite3.Connection,
    table: str,
    columns: dict[str, str],
) -> None:
    """Eski jadvalga yetishmayotgan ustunlarni xavfsiz qo‘shadi."""

    existing = {
        row["name"]
        for row in con.execute(
            f"PRAGMA table_info({table})"
        ).fetchall()
    }

    for column_name, definition in columns.items():
        if column_name not in existing:
            con.execute(
                f"ALTER TABLE {table} "
                f"ADD COLUMN {column_name} {definition}"
            )


def init_db() -> None:
    """
    Barcha jadvallarni yaratadi va eski bazani yangilaydi.

    Mavjud foydalanuvchi ma'lumotlarini o‘chirmaydi.
    """

    path = _database_path()

    with get_connection() as con:
        con.execute("PRAGMA journal_mode = WAL")

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
                created_at TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT ''
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
                updated_at TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS tasbeh (
                user_id INTEGER PRIMARY KEY,
                total_count INTEGER NOT NULL DEFAULT 0,
                daily_count INTEGER NOT NULL DEFAULT 0,
                last_date TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS quiz_stats (
                user_id INTEGER PRIMARY KEY,
                total_questions INTEGER NOT NULL DEFAULT 0,
                correct_answers INTEGER NOT NULL DEFAULT 0,
                score INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL DEFAULT '',
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
                created_at TEXT NOT NULL DEFAULT '',
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
                created_at TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(user_id)
                    REFERENCES users(user_id)
                    ON DELETE CASCADE
            );
            """
        )

        # Eski jadvallardagi yetishmayotgan ustunlarni qo‘shish.
        _add_missing_columns(
            con,
            "users",
            {
                "username": "TEXT",
                "first_name": "TEXT NOT NULL DEFAULT ''",
                "last_name": "TEXT NOT NULL DEFAULT ''",
                "language_code": "TEXT NOT NULL DEFAULT 'uz'",
                "is_active": "INTEGER NOT NULL DEFAULT 1",
                "is_subscribed": "INTEGER NOT NULL DEFAULT 0",
                "created_at": "TEXT NOT NULL DEFAULT ''",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
            },
        )

        _add_missing_columns(
            con,
            "user_settings",
            {
                "country": "TEXT NOT NULL DEFAULT ''",
                "city": "TEXT NOT NULL DEFAULT ''",
                "timezone": "TEXT NOT NULL DEFAULT 'Asia/Almaty'",
                "prayer_method": "INTEGER NOT NULL DEFAULT 3",
                "reminders_enabled": "INTEGER NOT NULL DEFAULT 0",
                "morning_reminder": "TEXT NOT NULL DEFAULT '08:00'",
                "evening_reminder": "TEXT NOT NULL DEFAULT '20:00'",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
            },
        )

        _add_missing_columns(
            con,
            "tasbeh",
            {
                "total_count": "INTEGER NOT NULL DEFAULT 0",
                "daily_count": "INTEGER NOT NULL DEFAULT 0",
                "last_date": "TEXT NOT NULL DEFAULT ''",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
            },
        )

        _add_missing_columns(
            con,
            "quiz_stats",
            {
                "total_questions": "INTEGER NOT NULL DEFAULT 0",
                "correct_answers": "INTEGER NOT NULL DEFAULT 0",
                "score": "INTEGER NOT NULL DEFAULT 0",
                "updated_at": "TEXT NOT NULL DEFAULT ''",
            },
        )

        _add_missing_columns(
            con,
            "quiz_attempts",
            {
                "question_id": "TEXT NOT NULL DEFAULT ''",
                "is_correct": "INTEGER NOT NULL DEFAULT 0",
                "points": "INTEGER NOT NULL DEFAULT 0",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
        )

        _add_missing_columns(
            con,
            "reminders",
            {
                "reminder_type": "TEXT NOT NULL DEFAULT 'general'",
                "message": "TEXT NOT NULL DEFAULT ''",
                "scheduled_at": "TEXT NOT NULL DEFAULT ''",
                "sent_at": "TEXT",
                "status": "TEXT NOT NULL DEFAULT 'pending'",
                "created_at": "TEXT NOT NULL DEFAULT ''",
            },
        )

        # Eski yozuvlarning bo‘sh vaqt maydonlarini to‘ldirish.
        now = utc_now()

        con.execute(
            """
            UPDATE users
            SET created_at = ?
            WHERE created_at = ''
            """,
            (now,),
        )

        con.execute(
            """
            UPDATE users
            SET updated_at = ?
            WHERE updated_at = ''
            """,
            (now,),
        )

        con.execute(
            """
            UPDATE user_settings
            SET updated_at = ?
            WHERE updated_at = ''
            """,
            (now,),
        )

        con.execute(
            """
            UPDATE tasbeh
            SET updated_at = ?
            WHERE updated_at = ''
            """,
            (now,),
        )

        con.execute(
            """
            UPDATE quiz_stats
            SET updated_at = ?
            WHERE updated_at = ''
            """,
            (now,),
        )

        con.execute(
            """
            UPDATE reminders
            SET created_at = ?
            WHERE created_at = ''
            """,
            (now,),
        )

        # Indekslar.
        con.executescript(
            """
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

    # Bazaga tegishli jadvallar tayyor.
    _ = path


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

    _validate_user_id(user_id)

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
    """Foydalanuvchi va barcha sozlamalarini qaytaradi."""

    _validate_user_id(user_id)

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
    """Kanal obunasi holatini saqlaydi."""

    _validate_user_id(user_id)

    with get_connection() as con:
        cursor = con.execute(
            """
            UPDATE users
            SET is_subscribed = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                int(bool(subscribed)),
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

    _validate_user_id(user_id)

    if not isinstance(country, str) or not isinstance(city, str):
        raise ValueError("Davlat va shahar matn bo‘lishi kerak.")

    country = country.strip()
    city = city.strip()

    if not country or not city:
        raise ValueError(
            "Davlat va shahar nomi bo‘sh bo‘lmasligi kerak."
        )

    if len(country) > 100 or len(city) > 100:
        raise ValueError("Shahar yoki davlat nomi juda uzun.")

    selected_timezone = _validate_timezone(
        timezone_name or settings.timezone
    )

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

    _validate_user_id(user_id)
    _validate_prayer_method(method)

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
# ESLATMALAR SOZLAMALARI
# =========================================================

def set_reminders(
    user_id: int,
    enabled: bool,
    morning: str | None = None,
    evening: str | None = None,
) -> None:
    """Tonggi va kechki eslatmalar sozlamalarini saqlaydi."""

    _validate_user_id(user_id)

    if not isinstance(enabled, bool):
        raise ValueError("Eslatma holati True yoki False bo‘lishi kerak.")

    morning_time = _validate_reminder_time(
        morning if morning is not None else settings.morning_reminder
    )

    evening_time = _validate_reminder_time(
        evening if evening is not None else settings.evening_reminder
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
                int(enabled),
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

    _validate_user_id(user_id)

    if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:
        raise ValueError("Miqdor musbat butun son bo‘lishi kerak.")

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
            total = 0
            daily = 0

            con.execute(
                """
                INSERT INTO tasbeh (
                    user_id,
                    updated_at
                )
                VALUES (?, ?)
                """,
                (user_id, now),
            )
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

    _validate_user_id(user_id)

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
            INSERT OR IGNORE INTO tasbeh (
                user_id,
                updated_at
            )
            VALUES (?, ?)
            """,
            (user_id, utc_now()),
        )

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
# SIYRAT / VIKTORINA
# =========================================================

def add_quiz_result(
    user_id: int,
    question_id: str,
    is_correct: bool,
    points: int = 20,
) -> dict[str, int]:
    """Viktorina natijasi va ballarini saqlaydi."""

    _validate_user_id(user_id)

    if not isinstance(question_id, str) or not question_id.strip():
        raise ValueError("Savol ID bo‘sh bo‘lmasligi kerak.")

    if len(question_id) > 100:
        raise ValueError("Savol ID juda uzun.")

    if not isinstance(is_correct, bool):
        raise ValueError("Javob holati True yoki False bo‘lishi kerak.")

    if isinstance(points, bool) or not isinstance(points, int) or points < 0:
        raise ValueError("Ball manfiy bo‘lmagan butun son bo‘lishi kerak.")

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
                question_id.strip(),
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
        raise RuntimeError("Viktorina natijasi topilmadi.")

    return dict(row)


def get_leaderboard(
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Eng ko‘p ball to‘plagan faol foydalanuvchilar."""

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("Limit butun son bo‘lishi kerak.")

    if not 1 <= limit <= 100:
        raise ValueError("Limit 1 dan 100 gacha bo‘lishi kerak.")

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
    """Yangi eslatmani bazaga qo‘shadi."""

    _validate_user_id(user_id)

    if not isinstance(reminder_type, str) or not reminder_type.strip():
        raise ValueError("Eslatma turi bo‘sh bo‘lmasligi kerak.")

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Eslatma matni bo‘sh bo‘lmasligi kerak.")

    if len(reminder_type) > 50 or len(message) > 4000:
        raise ValueError("Eslatma ma'lumotlari juda uzun.")

    scheduled_value = _validate_scheduled_at(scheduled_at)

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
                scheduled_value,
                utc_now(),
            ),
        )

        return int(cursor.lastrowid)


def get_pending_reminders(
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Yuborilishi kutilayotgan eslatmalarni qaytaradi."""

    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ValueError("Limit butun son bo‘lishi kerak.")

    if not 1 <= limit <= 1000:
        raise ValueError("Limit 1 dan 1000 gacha bo‘lishi kerak.")

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

    if isinstance(reminder_id, bool) or not isinstance(reminder_id, int) or reminder_id <= 0:
        raise ValueError("Eslatma ID noto‘g‘ri.")

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

    if isinstance(reminder_id, bool) or not isinstance(reminder_id, int) or reminder_id <= 0:
        raise ValueError("Eslatma ID noto‘g‘ri.")

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

    _validate_user_id(user_id)

    with get_connection() as con:
        cursor = con.execute(
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

        if cursor.rowcount == 0:
            raise ValueError("Foydalanuvchi topilmadi.")


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
