from app.core.constants import API_V1_PREFIX


def test_eval_run_creates_and_returns_completed(client):
    """POST /eval/run creates an eval and runs it, returns completed."""
    payload = {"run_id": "run_abc123", "suite": "smoke"}
    response = client.post(f"{API_V1_PREFIX}/eval/run", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["eval_id"].startswith("eval_")
    assert data["run_id"] == "run_abc123"
    assert data["status"] == "completed"
    assert "created_at" in data
    assert data.get("started_at")
    assert data.get("finished_at")
    assert data.get("results")["failed"] == 1
    assert "metrics" in data


def test_eval_run_passes_when_run_exists(client):
    """POST /eval/run with valid run_id returns passed when run exists and is completed."""
    run_resp = client.post(
        f"{API_V1_PREFIX}/runs",
        json={"workflow_id": "wf1", "input": {"text": "test"}},
    )
    assert run_resp.status_code == 200
    run_id = run_resp.json()["run_id"]
    eval_resp = client.post(
        f"{API_V1_PREFIX}/eval/run",
        json={"run_id": run_id},
    )
    assert eval_resp.status_code == 200
    assert eval_resp.json()["results"]["passed"] == 1
    assert eval_resp.json()["results"]["failed"] == 0


def test_eval_get_returns_run(client):
    """GET /eval/{id} returns the evaluation run after creation."""
    create_resp = client.post(f"{API_V1_PREFIX}/eval/run", json={})
    assert create_resp.status_code == 200
    eval_id = create_resp.json()["eval_id"]

    get_resp = client.get(f"{API_V1_PREFIX}/eval/{eval_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["eval_id"] == eval_id
    assert get_resp.json()["status"] == "completed"


def test_eval_get_404_for_unknown_id(client):
    """GET /eval/{id} returns 404 for unknown eval_id."""
    response = client.get(f"{API_V1_PREFIX}/eval/eval_nonexistent")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
