def test_version_endpoint(client):
    """Test that version endpoint returns API version information."""
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert "api_version" in data


