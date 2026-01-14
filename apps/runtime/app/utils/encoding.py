"""Encoding utilities."""

import base64


def base64_encode(data: str) -> str:
    """Encode string to base64."""
    return base64.b64encode(data.encode()).decode()


def base64_decode(data: str) -> str:
    """Decode base64 string."""
    return base64.b64decode(data.encode()).decode()

