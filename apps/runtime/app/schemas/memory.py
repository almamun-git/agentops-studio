"""Memory-related schemas."""

from pydantic import BaseModel, Field

from app.models.core import MemoryItem


class MemoryItemIn(BaseModel):
    """Memory item payload for upsert."""
    key: str = Field(..., min_length=1, description="Memory key.")
    value: dict = Field(..., description="Stored value.")
    metadata: dict | None = Field(default=None, description="Optional metadata.")


class MemoryUpsertRequest(BaseModel):
    """Request schema for upserting memory items."""
    items: list[MemoryItemIn] = Field(..., min_length=1, description="Items to upsert.")


class MemoryResponse(BaseModel):
    """Memory response schema."""
    user_id: str
    items: list[MemoryItem]


class MemoryUpsertResponse(BaseModel):
    """Response schema for memory upsert."""
    user_id: str
    items: list[MemoryItem]


class MemoryDeleteResponse(BaseModel):
    """Response schema for memory delete."""
    memory_id: str
    deleted: bool = True

