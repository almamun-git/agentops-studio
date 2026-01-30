from fastapi import APIRouter, Depends

from app.schemas.rag import RagIngestRequest, RagIngestResponse, RagQueryRequest, RagQueryResponse
from app.services.rag_service import RagService, get_rag_service

router = APIRouter()


@router.post("/ingest", response_model=RagIngestResponse)
async def ingest_documents(
    payload: RagIngestRequest,
    rag: RagService = Depends(get_rag_service),
) -> RagIngestResponse:
    """Ingest documents for RAG retrieval."""
    documents = await rag.ingest(payload.user_id, payload.documents)
    return RagIngestResponse(user_id=payload.user_id, documents=documents)


@router.post("/query", response_model=RagQueryResponse)
async def query_documents(
    payload: RagQueryRequest,
    rag: RagService = Depends(get_rag_service),
) -> RagQueryResponse:
    """Query RAG documents for a user."""
    matches = await rag.query(payload.user_id, payload.query, payload.top_k)
    return RagQueryResponse(user_id=payload.user_id, query=payload.query, matches=matches)
