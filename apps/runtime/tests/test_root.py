def test_root_endpoint(client):
    """Test that root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AgentOps Runtime"
    assert data["version"] == "0.1.0"
    assert "docs" in data
    assert data["api_base"] == "/api/v1"
    assert data["version_endpoint"] == "/api/v1/version"

