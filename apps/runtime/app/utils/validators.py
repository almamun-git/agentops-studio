"""Validation utilities."""


def validate_api_key(api_key: str | None) -> bool:
    """Validate API key format."""
    if not api_key:
        return False
    return len(api_key) > 10


def validate_url(url: str) -> bool:
    """Basic URL validation."""
    return url.startswith(("http://", "https://"))

