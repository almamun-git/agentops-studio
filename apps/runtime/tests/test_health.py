def test_health_endpoint(client):
    """Test that health endpoint returns 200 OK with expected fields."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data

