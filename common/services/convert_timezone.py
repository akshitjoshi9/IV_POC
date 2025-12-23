from datetime import datetime
import pytz
from typing import Optional, Union
from fastapi import Header, Depends

TIMEZONE_ALIASES = {
    "Asia/Calcutta": "Asia/Kolkata",
    "Calcutta": "Asia/Kolkata",
}


def get_user_timezone(client_timezone: str = Header("UTC", alias="client-timezone")) -> pytz.BaseTzInfo:
    """Return pytz timezone object from FE header."""
    # Normalize alias if needed
    tz = TIMEZONE_ALIASES.get(client_timezone, client_timezone)
    try:
        return pytz.timezone(tz)
    except pytz.UnknownTimeZoneError:
        return pytz.UTC

def convert_to_user_timezone(dt: Optional[datetime], user_tz: Union[str, pytz.BaseTzInfo]) -> Optional[datetime]:
    """
    Convert DB datetime to user's timezone.
    Works for naive (assume UTC).
    """
    if dt is None:
        return None

    # Only localize if naive
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=pytz.UTC)

    # Convert to pytz object if string
    if isinstance(user_tz, str):
        user_tz = pytz.timezone(user_tz)

    return dt.astimezone(user_tz)
