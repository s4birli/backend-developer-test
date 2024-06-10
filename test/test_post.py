import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def token(client: TestClient, new_user):
    response = client.post("/auth/login", json=new_user)
    return response.json()["access_token"]

@pytest.fixture
def new_post():
    return {"text": "This is a test post"}

def test_add_post(client: TestClient, token: str, new_post):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/posts/addpost", json=new_post, headers=headers)
    assert response.status_code == 200
    assert response.json()["text"] == new_post["text"]

def test_get_posts(client: TestClient, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/posts/posts", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_post(client: TestClient, token: str, new_post):
    headers = {"Authorization": f"Bearer {token}"}
    add_post_response = client.post("/posts/addpost", json=new_post, headers=headers)
    post_id = add_post_response.json()["id"]
    delete_post_response = client.delete(f"/posts/deletepost/{post_id}", headers=headers)
    assert delete_post_response.status_code == 200
    assert delete_post_response.json()["detail"] == "Post deleted"
