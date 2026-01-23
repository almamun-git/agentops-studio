from app.core.constants import API_V1_PREFIX


def test_health_endpoint(client):
    """Test that health endpoint returns 200 OK with expected fields."""
    response = client.get(f"{API_V1_PREFIX}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert data["timestamp"].endswith("+00:00")

