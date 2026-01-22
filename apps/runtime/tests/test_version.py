from app.core.constants import API_V1_PREFIX
from app.core.metadata import API_VERSION, APP_VERSION


def test_version_endpoint(client):
    """Test that version endpoint returns API version information."""
    response = client.get(f"{API_V1_PREFIX}/version")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == APP_VERSION
    assert data["api_version"] == API_VERSION


