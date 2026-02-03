from app.core.constants import API_V1_PREFIX


def test_rag_ingest_and_query(client):
    ingest_payload = {
        "user_id": "user-99",
        "documents": [
            {"text": "Vector databases store embeddings", "metadata": {"source": "docs"}},
            {"text": "Retrieval augmented generation overview", "metadata": {"source": "blog"}},
        ],
    }
    ingest_response = client.post(f"{API_V1_PREFIX}/rag/ingest", json=ingest_payload)
    assert ingest_response.status_code == 200
    data = ingest_response.json()
    assert data["user_id"] == "user-99"
    assert len(data["documents"]) == 2
    assert data["documents"][0]["created_at"]

    query_payload = {"user_id": "user-99", "query": "retrieval generation", "top_k": 2, "min_score": 0.5}
    query_response = client.post(f"{API_V1_PREFIX}/rag/query", json=query_payload)
    assert query_response.status_code == 200
    query_data = query_response.json()
    assert query_data["user_id"] == "user-99"
    assert query_data["query"] == "retrieval generation"
    assert query_data["matches"]

    doc_id = data["documents"][0]["doc_id"]
    delete_response = client.delete(f"{API_V1_PREFIX}/rag/{doc_id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["doc_id"] == doc_id
    assert delete_data["deleted"] is True
