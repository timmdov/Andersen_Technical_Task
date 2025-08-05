import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_auth_token():
    user_data = {
        "username": "testuser",
        "password": "testpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    client.post("/api/auth/register", json=user_data)
    # Login and get token
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/api/auth/login", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]

@pytest.fixture(scope="module")
def auth_header():
    token = get_auth_token()
    return {"Authorization": f"Bearer {token}"}


def test_create_task(auth_header):
    data = {
        "title": "My test task",
        "description": "This is a test.",
        "status": "NEW"
    }
    resp = client.post("/api/tasks/", json=data, headers=auth_header)
    assert resp.status_code == 201
    res = resp.json()
    assert res["title"] == "My test task"
    assert res["status"] == "NEW"
    global created_task_id
    created_task_id = res["id"]

def test_get_tasks(auth_header):
    resp = client.get("/api/tasks/", headers=auth_header)
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert data["page"] == 1

def test_update_task(auth_header):
    resp = client.get("/api/tasks/", headers=auth_header)
    task_id = resp.json()["items"][0]["id"]
    update_data = {
        "title": "Updated task title"
    }
    resp = client.put(f"/api/tasks/{task_id}", json=update_data, headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated task title"

def test_mark_complete(auth_header):
    resp = client.get("/api/tasks/", headers=auth_header)
    task_id = resp.json()["items"][0]["id"]
    resp = client.patch(f"/api/tasks/{task_id}/complete", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["status"] == "COMPLETED"

def test_delete_task(auth_header):
    resp = client.get("/api/tasks/", headers=auth_header)
    task_id = resp.json()["items"][0]["id"]
    resp = client.delete(f"/api/tasks/{task_id}", headers=auth_header)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Task deleted"