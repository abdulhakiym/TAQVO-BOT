"""TAQVO BOT services package."""

from bot.services.prayer import (
    PrayerAPIError,
    get_prayer_times,
    get_today_prayer_times,
)

from bot.services.timezone import (
    convert_local_to_utc,
    convert_utc_to_local,
    get_local_now,
    get_timezone,
    get_timezone_offset,
    is_valid_timezone,
)

from bot.services.user_service import (
    deactivate_user,
    get_user_by_telegram_id,
    register_or_update_user,
    update_user_preferences,
)


__all__ = [
    "PrayerAPIError",
    "get_prayer_times",
    "get_today_prayer_times",
    "convert_local_to_utc",
    "convert_utc_to_local",
    "get_local_now",
    "get_timezone",
    "get_timezone_offset",
    "is_valid_timezone",
    "deactivate_user",
    "get_user_by_telegram_id",
    "register_or_update_user",
    "update_user_preferences",
]
