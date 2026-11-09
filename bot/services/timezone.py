"""TAQVO BOT timezone utilities."""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def is_valid_timezone(
    timezone_name: str,
) -> bool:
    """Check whether a timezone name is valid."""

    if not timezone_name or not timezone_name.strip():
        return False

    try:
        ZoneInfo(timezone_name.strip())
        return True

    except (ZoneInfoNotFoundError, ValueError):
        return False


def get_timezone(
    timezone_name: str,
) -> ZoneInfo:
    """Return a validated timezone."""

    if not is_valid_timezone(timezone_name):
        raise ValueError(
            f"Noto'g'ri vaqt mintaqasi: {timezone_name}"
        )

    return ZoneInfo(timezone_name.strip())


def get_local_now(
    timezone_name: str,
) -> datetime:
    """Get current local date and time."""

    return datetime.now(
        get_timezone(timezone_name)
    )


def convert_utc_to_local(
    value: datetime,
    timezone_name: str,
) -> datetime:
    """Convert timezone-aware datetime to local time."""

    if value.tzinfo is None:
        raise ValueError(
            "Datetime timezone ma'lumotiga ega bo'lishi kerak."
        )

    return value.astimezone(
        get_timezone(timezone_name)
    )


def convert_local_to_utc(
    value: datetime,
    timezone_name: str,
) -> datetime:
    """Convert local datetime to UTC."""

    if value.tzinfo is not None:
        raise ValueError(
            "Mahalliy datetime timezone'siz bo'lishi kerak."
        )

    local_time = value.replace(
        tzinfo=get_timezone(timezone_name)
    )

    return local_time.astimezone(timezone.utc)


def get_timezone_offset(
    timezone_name: str,
) -> str:
    """Return UTC offset, for example +05:00."""

    offset = get_local_now(
        timezone_name
    ).strftime("%z")

    if len(offset) != 5:
        return offset

    return f"{offset[:3]}:{offset[3:]}"
