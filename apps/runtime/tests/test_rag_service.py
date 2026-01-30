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
