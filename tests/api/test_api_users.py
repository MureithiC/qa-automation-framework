import pytest
from utils.api_client import APIClient

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture
def api():
    return APIClient(BASE_URL)


class TestGetPosts:
    def test_get_all_posts_returns_200(self, api):
        response = api.get("/posts")
        assert response.status_code == 200

    def test_get_all_posts_returns_list(self, api):
        data = api.get("/posts").json()
        assert isinstance(data, list)
        assert len(data) == 100

    def test_get_single_post_returns_200(self, api):
        assert api.get("/posts/1").status_code == 200

    def test_get_single_post_correct_id(self, api):
        data = api.get("/posts/1").json()
        assert data["id"] == 1

    def test_get_nonexistent_post_returns_404(self, api):
        assert api.get("/posts/9999").status_code == 404

    def test_get_post_has_required_fields(self, api):
        data = api.get("/posts/1").json()
        assert "id" in data
        assert "title" in data
        assert "body" in data
        assert "userId" in data


class TestCreatePost:
    def test_create_post_returns_201(self, api):
        payload = {"title": "QA Test Post", "body": "Automated test", "userId": 1}
        response = api.post("/posts", json=payload)
        assert response.status_code == 201

    def test_create_post_returns_correct_data(self, api):
        payload = {"title": "QA Test Post", "body": "Automated test", "userId": 1}
        data = api.post("/posts", json=payload).json()
        assert data["title"] == "QA Test Post"
        assert data["body"] == "Automated test"
        assert "id" in data


class TestUpdatePost:
    def test_update_post_returns_200(self, api):
        payload = {"title": "Updated Title", "body": "Updated body", "userId": 1}
        response = api.put("/posts/1", json=payload)
        assert response.status_code == 200

    def test_update_post_reflects_changes(self, api):
        payload = {"title": "Updated Title", "body": "Updated body", "userId": 1}
        data = api.put("/posts/1", json=payload).json()
        assert data["title"] == "Updated Title"


class TestGetUsers:
    def test_get_users_returns_200(self, api):
        assert api.get("/users").status_code == 200

    def test_get_users_returns_list(self, api):
        data = api.get("/users").json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_single_user_returns_200(self, api):
        assert api.get("/users/1").status_code == 200

    def test_get_single_user_has_email(self, api):
        data = api.get("/users/1").json()
        assert "email" in data
        assert "@" in data["email"]
