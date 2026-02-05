"""Common schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class StatusResponse(BaseModel):
    """Status response schema."""
    status: Literal["ok", "error"] = Field(..., description="Service status.")
    timestamp: str = Field(..., description="ISO-8601 UTC timestamp.")


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    code: str | None = None


class RootResponse(BaseModel):
    """Root endpoint response schema."""
    name: str
    version: str
    docs: str
    api_base: str
    version_endpoint: str


class VersionResponse(BaseModel):
    """Version endpoint response schema."""
    version: str
    api_version: str


__all__ = [
    "ErrorResponse",
    "RootResponse",
    "StatusResponse",
    "VersionResponse",
]

