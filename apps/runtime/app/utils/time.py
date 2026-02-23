"""Time utilities."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Get current UTC datetime (timezone.utc for 3.10 compatibility)."""
    return datetime.now(timezone.utc)


def format_timestamp(dt: datetime) -> str:
    """Format datetime as ISO string."""
    return dt.isoformat()

