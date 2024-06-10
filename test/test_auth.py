import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def new_user():
    return {"email": "test@example.com", "password": "testpassword"}

def test_signup(client: TestClient, new_user):
    response = client.post("/auth/signup", json=new_user)
    assert response.status_code == 200
    assert response.json()["email"] == new_user["email"]

def test_login(client: TestClient, new_user):
    response = client.post("/auth/login", json=new_user)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
