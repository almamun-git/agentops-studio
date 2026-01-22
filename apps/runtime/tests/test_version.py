from app.core.metadata import API_VERSION, APP_VERSION


def test_version_endpoint(client):
    """Test that version endpoint returns API version information."""
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == APP_VERSION
    assert data["api_version"] == API_VERSION


