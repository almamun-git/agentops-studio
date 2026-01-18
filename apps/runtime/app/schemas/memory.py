"""Memory-related schemas."""

from pydantic import BaseModel

from app.models.core import MemoryItem


class MemoryResponse(BaseModel):
    """Memory response schema."""
    user_id: str
    items: list[MemoryItem]

