import json
import pytest
from app.api import crud_regions


# Test creating region
def test_create_region(test_app, monkeypatch):
    test_request_payload = {"title": "Казанская область"}
    test_response_payload = {"id": 1, "title": "Казанская область"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud_regions, "post", mock_post)
    response = test_app.post("/regions/", data=json.dumps(test_request_payload),)
    assert response.status_code == 201
    assert response.json() == test_response_payload


# Test creating invalid region
def test_create_region_invalid_json(test_app):
    response = test_app.post("/regions/", data=json.dumps({"title": ""}))
    assert response.status_code == 422
    response = test_app.post("/regions/", data=json.dumps({"title": "1", "description": "2"}))
    assert response.status_code == 422


# Test getting region from table
def test_get_region(test_app, monkeypatch):
    test_data = {"id": 1, "title": "something"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud_regions, "get_by_id", mock_get)
    response = test_app.get("/regions/1")
    assert response.status_code == 200
    assert response.json() == test_data


# Test getting region with incorrect id from table
def test_get_region_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud_regions, "get_by_id", mock_get)
    response = test_app.get("/regions/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
    response = test_app.get("/regions/0")
    assert response.status_code == 422


# Test getting region from table
def test_read_all_regions(test_app, monkeypatch):
    test_data = [
        {"title": "something", "id": 1},
        {"title": "someone", "id": 2},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(crud_regions, "get_all", mock_get_all)
    response = test_app.get("/regions/")
    assert response.status_code == 200
    assert response.json() == test_data


# Test updating region
def test_update_region(test_app, monkeypatch):
    test_update_data = {"title": "someone", "id": 1}

    async def mock_get(id):
        return True

    monkeypatch.setattr(crud_regions, "get_by_id", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(crud_regions, "put", mock_put)
    response = test_app.put("/regions/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


# Test invalid updating region
@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"title": "1"}, 422],
        [0, {"title": "foo"}, 422],
    ],
)
def test_update_region_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud_regions, "get_by_id", mock_get)
    response = test_app.put(f"/regions/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


# Test removing region
def test_remove_region(test_app, monkeypatch):
    test_data = {"title": "something", "id": 1}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud_regions, "get_by_id", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud_regions, "delete_by_id", mock_delete)
    response = test_app.delete("/regions/1/")
    assert response.status_code == 200
    assert response.json() == test_data


# Test incorrect removing region
def test_remove_region_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud_regions, "get_by_id", mock_get)
    response = test_app.delete("/regions/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"
    response = test_app.delete("/regions/0/")
    assert response.status_code == 422
