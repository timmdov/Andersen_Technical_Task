from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_login_and_protected_route():
    # Clean test user, in case test DB is reused
    username = "auth_test_user"
    password = "secure123"
    register_resp = client.post("/api/auth/register", json={
        "username": username,
        "password": password
    })
    # Registration can return 201 (created) or 409 (conflict, already exists) if not resetting DB each time
    assert register_resp.status_code in [201, 409]

    # Login with correct credentials
    login_resp = client.post("/api/auth/login", data={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200, login_resp.text
    login_data = login_resp.json()
    assert "access_token" in login_data
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Access a protected endpoint (get own tasks, should work)
    tasks_resp = client.get("/api/tasks/", headers=headers)
    assert tasks_resp.status_code == 200

    # Try protected endpoint without token (should fail)
    unauth_resp = client.get("/api/tasks/")
    assert unauth_resp.status_code == 401

def test_register_twice_should_fail():
    username = "double_register"
    password = "test"
    resp1 = client.post("/api/auth/register", json={"username": username, "password": password})
    resp2 = client.post("/api/auth/register", json={"username": username, "password": password})
    assert resp2.status_code == 409 or resp2.status_code == 400

def test_invalid_login():
    # Non-existent user
    resp = client.post("/api/auth/login", data={
        "username": "nonexistentuser",
        "password": "whatever"
    })
    assert resp.status_code == 401

    # Wrong password for real user
    client.post("/api/auth/register", json={"username": "badpass", "password": "right"})
    resp = client.post("/api/auth/login", data={"username": "badpass", "password": "wrong"})
    assert resp.status_code == 401

def test_password_is_hashed_in_db():
    # This test assumes you can access your DB directly.
    # This is a pseudo-example, update according to your DB/ORM setup.
    from app.db.base import SessionLocal
    from app.users.models import User

    username = "hashcheck"
    password = "plainsecret"
    client.post("/api/auth/register", json={"username": username, "password": password})

    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    assert user is not None
    assert user.password_hash != password  # The password in DB is not plain text
    assert user.password_hash.startswith("$2b$") or user.password_hash.startswith("$2a$")  # bcrypt hash prefix