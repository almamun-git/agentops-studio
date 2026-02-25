from app.core.constants import API_V1_PREFIX


def test_create_run_returns_run(client):
    """POST /runs creates a run and returns run details."""
    response = client.post(
        f"{API_V1_PREFIX}/runs",
        json={"workflow_id": "wf1", "input": {"text": "hello"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["run_id"]
    assert data["workflow_id"] == "wf1"
    assert data["status"] == "completed"
    assert "steps" in data


def test_get_run_404_for_unknown_id(client):
    """GET /runs/{run_id} returns 404 when run does not exist."""
    response = client.get(f"{API_V1_PREFIX}/runs/run_nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
