"""Common schemas."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """Status response schema."""
    status: Literal["ok", "error"]
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    code: str | None = None

