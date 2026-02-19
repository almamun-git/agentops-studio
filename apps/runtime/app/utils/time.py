"""Time utilities."""

from datetime import datetime


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(datetime.UTC)


def format_timestamp(dt: datetime) -> str:
    """Format datetime as ISO string."""
    return dt.isoformat()

