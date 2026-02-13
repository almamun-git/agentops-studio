from app.core.constants import API_V1_PREFIX


def test_memory_get_empty(client):
    """GET /memory/{user_id} returns empty items for new user."""
    response = client.get(f"{API_V1_PREFIX}/memory/user-1")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user-1"
    assert data["items"] == []


def test_memory_upsert_and_get(client):
    """PUT /memory/{user_id} upserts items, GET returns them."""
    payload = {
        "items": [
            {"key": "preference", "value": {"theme": "dark"}},
            {"key": "last_topic", "value": {"topic": "evals"}},
        ]
    }
    put_resp = client.put(f"{API_V1_PREFIX}/memory/user-2", json=payload)
    assert put_resp.status_code == 200
    put_data = put_resp.json()
    assert put_data["user_id"] == "user-2"
    assert len(put_data["items"]) == 2
    assert put_data["items"][0]["memory_id"].startswith("mem_")
    assert put_data["items"][0]["key"] == "preference"
    assert put_data["items"][0]["value"] == {"theme": "dark"}

    get_resp = client.get(f"{API_V1_PREFIX}/memory/user-2")
    assert get_resp.status_code == 200
    get_data = get_resp.json()
    assert len(get_data["items"]) == 2
    keys = {i["key"] for i in get_data["items"]}
    assert keys == {"preference", "last_topic"}


def test_memory_delete(client):
    """DELETE /memory/{user_id}/{memory_id} removes the item."""
    put_resp = client.put(
        f"{API_V1_PREFIX}/memory/user-3",
        json={"items": [{"key": "temp", "value": {"x": 1}}]},
    )
    assert put_resp.status_code == 200
    memory_id = put_resp.json()["items"][0]["memory_id"]

    del_resp = client.delete(f"{API_V1_PREFIX}/memory/user-3/{memory_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["memory_id"] == memory_id
    assert del_resp.json()["deleted"] is True

    get_resp = client.get(f"{API_V1_PREFIX}/memory/user-3")
    assert get_resp.status_code == 200
    assert len(get_resp.json()["items"]) == 0
