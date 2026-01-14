"""Memory-related schemas."""

from pydantic import BaseModel


class MemoryItem(BaseModel):
    """Memory item schema."""
    key: str
    value: dict
    metadata: dict | None = None


class MemoryResponse(BaseModel):
    """Memory response schema."""
    user_id: str
    items: list[MemoryItem]

