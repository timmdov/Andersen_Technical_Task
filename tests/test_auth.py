import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

REGISTER_URL = "/api/auth/register"
LOGIN_URL = "/api/auth/login"

def test_register_and_login_success():
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "password": "strongpassword"
    }
    response = client.post(REGISTER_URL, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "johndoe"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert "id" in data
    login_data = {
        "username": "johndoe",
        "password": "strongpassword"
    }
    response = client.post(LOGIN_URL, data=login_data)
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_register_duplicate_username():
    payload = {
        "first_name": "Jane",
        "last_name": "Smith",
        "username": "janesmith",
        "password": "password123"
    }
    response1 = client.post(REGISTER_URL, json=payload)
    assert response1.status_code == 201
    response2 = client.post(REGISTER_URL, json=payload)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Username already exists."

def test_register_invalid_password():
    payload = {
        "first_name": "Short",
        "last_name": "Pwd",
        "username": "shortpwd",
        "password": "123"
    }
    response = client.post(REGISTER_URL, json=payload)
    assert response.status_code == 422

def test_login_wrong_password():
    payload = {
        "first_name": "Alice",
        "last_name": "Wonderland",
        "username": "alice",
        "password": "securepass"
    }
    client.post(REGISTER_URL, json=payload)
    login_data = {
        "username": "alice",
        "password": "wrongpassword"
    }
    response = client.post(LOGIN_URL, data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_nonexistent_user():
    login_data = {
        "username": "ghost",
        "password": "irrelevant"
    }
    response = client.post(LOGIN_URL, data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"