from app.core.constants import API_V1_PREFIX


def test_root_endpoint(client):
    """Test that root endpoint returns API information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AgentOps Runtime"
    assert data["version"] == "0.1.0"
    assert "docs" in data
    assert data["api_base"] == API_V1_PREFIX
    assert data["version_endpoint"] == f"{API_V1_PREFIX}/version"

