"""Response utilities."""

from typing import Any

from fastapi.responses import JSONResponse


def success_response(data: Any, status_code: int = 200) -> JSONResponse:
    """Create a success response."""
    return JSONResponse(
        status_code=status_code,
        content={"success": True, "data": data},
    )


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Create an error response."""
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "error": message},
    )

