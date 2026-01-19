from datetime import datetime, timezone

import pytest

from app.adapters.inmemory_vector import InMemoryVectorStore
from app.models.core import MemoryItem


@pytest.mark.asyncio
async def test_inmemory_vector_store_upsert_query_delete():
    store = InMemoryVectorStore()
    item = MemoryItem(
        memory_id="mem-1",
        user_id="user-1",
        key="profile",
        value={"name": "Ada"},
        created_at=datetime.now(timezone.utc),
    )

    await store.upsert([item])

    matches = await store.query("user-1", "ada")
    assert matches == [item]

    await store.delete("mem-1")
    matches = await store.query("user-1", "ada")
    assert matches == []
