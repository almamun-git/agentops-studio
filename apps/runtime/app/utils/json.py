"""JSON utilities."""

import json
from typing import Any


def safe_json_loads(data: str) -> Any:
    """Safely parse JSON string."""
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None


def safe_json_dumps(data: Any) -> str:
    """Safely serialize to JSON string."""
    return json.dumps(data, default=str)

