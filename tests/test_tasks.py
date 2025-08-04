from fastapi.testclient import TestClient
from app.main import app
from app.tasks.schemas import TaskStatus

client = TestClient(app)


def register_user(username="testuser", password="testpass"):
    data = {"username": username, "password": password}
    resp = client.post("/api/auth/register", json=data)
    assert resp.status_code == 201
    return resp.json()

def login_user(username="testuser", password="testpass"):
    data = {"username": username, "password": password}
    resp = client.post("/api/auth/login", data=data)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}



def test_task_crud_flow():
    # Register and login user
    register_user("testuser", "testpass")
    token = login_user("testuser", "testpass")
    headers = auth_headers(token)

    # Create a task
    payload = {
        "title": "Buy milk",
        "description": "Get two bottles",
        "status": TaskStatus.NEW
    }
    resp = client.post("/api/tasks/", json=payload, headers=headers)
    assert resp.status_code == 201, resp.text
    task = resp.json()
    task_id = task["id"]
    assert task["title"] == "Buy milk"
    assert task["status"] == "NEW"

    # Get the created task
    resp = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert resp.status_code == 200
    task = resp.json()
    assert task["title"] == "Buy milk"

    # Update the task
    update_payload = {
        "title": "Buy milk and bread",
        "description": "Two bottles, one loaf",
        "status": TaskStatus.IN_PROGRESS
    }
    resp = client.put(f"/api/tasks/{task_id}", json=update_payload, headers=headers)
    assert resp.status_code == 200
    task = resp.json()
    assert task["title"] == "Buy milk and bread"
    assert task["status"] == "IN_PROGRESS"

    # Mark as complete (PATCH)
    resp = client.patch(f"/api/tasks/{task_id}/complete", headers=headers)
    assert resp.status_code == 200
    task = resp.json()
    assert task["status"] == "COMPLETED"

    # Get paginated list
    resp = client.get("/api/tasks/", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["items"], list)
    assert data["total"] >= 1

    # Delete the task
    resp = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Task deleted"

    # Get deleted task: should be 404
    resp = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert resp.status_code == 404

# ------------- More test ideas for robustness -------------

def test_unauthorized_access():
    # Should not allow access without token
    payload = {"title": "No auth", "description": "fail", "status": TaskStatus.NEW}
    resp = client.post("/api/tasks/", json=payload)
    assert resp.status_code == 401

def test_access_denied_to_other_users():
    # Create first user and a task
    register_user("user1", "pass1")
    token1 = login_user("user1", "pass1")
    headers1 = auth_headers(token1)
    resp = client.post("/api/tasks/", json={"title": "u1task", "description": "", "status": TaskStatus.NEW}, headers=headers1)
    task_id = resp.json()["id"]

    # Register a second user, try to delete other's task
    register_user("user2", "pass2")
    token2 = login_user("user2", "pass2")
    headers2 = auth_headers(token2)
    resp = client.delete(f"/api/tasks/{task_id}", headers=headers2)
    assert resp.status_code == 403

    # Clean up: user1 deletes their own task
    resp = client.delete(f"/api/tasks/{task_id}", headers=headers1)
    assert resp.status_code == 200