import pytest

from app.adapters.inmemory_vector import InMemoryVectorStore
from app.schemas.rag import RagDocumentIn
from app.services.rag_service import RagService


@pytest.mark.asyncio
async def test_rag_service_ingest_and_query():
    store = InMemoryVectorStore()
    service = RagService(store)

    documents = await service.ingest(
        "user-1",
        [
            RagDocumentIn(text="Apollo program mission notes", metadata={"source": "nasa"}),
            RagDocumentIn(text="Cooking tips for pasta", metadata={"source": "cookbook"}),
        ],
    )

    assert len(documents) == 2

    matches = await service.query("user-1", "apollo mission", top_k=2)

    assert matches
    assert matches[0].doc_id == documents[0].doc_id
    assert matches[0].created_at


@pytest.mark.asyncio
async def test_rag_service_metadata_match():
    store = InMemoryVectorStore()
    service = RagService(store)

    await service.ingest(
        "user-2",
        [
            RagDocumentIn(text="Short note", metadata={"source": "nasa"}),
        ],
    )

    matches = await service.query("user-2", "nasa", top_k=1)

    assert matches
    assert matches[0].metadata == {"source": "nasa"}


@pytest.mark.asyncio
async def test_rag_service_min_score_filter():
    store = InMemoryVectorStore()
    service = RagService(store)

    documents = await service.ingest(
        "user-3",
        [
            RagDocumentIn(text="apollo mission report"),
            RagDocumentIn(text="apollo report"),
        ],
    )

    matches = await service.query("user-3", "apollo mission", top_k=5, min_score=0.75)

    assert matches
    assert matches[0].doc_id == documents[0].doc_id
    assert all(match.score >= 0.75 for match in matches)


@pytest.mark.asyncio
async def test_rag_service_delete_removes_match():
    store = InMemoryVectorStore()
    service = RagService(store)

    documents = await service.ingest(
        "user-4",
        [
            RagDocumentIn(text="ocean exploration report"),
        ],
    )

    doc_id = documents[0].doc_id
    await service.delete(doc_id)

    matches = await service.query("user-4", "ocean", top_k=3)

    assert matches == []
