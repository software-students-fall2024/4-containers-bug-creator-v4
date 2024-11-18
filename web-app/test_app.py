import pytest
import json
import base64
from app import app


@pytest.fixture(name="test_client")
def fixture_test_client():
    """Mock client fixture"""
    with app.test_client() as client:
        yield client


@pytest.fixture(name="client")
def fixture_authenticated_client(test_client):
    """Fixture to authenticate a user for the dashboard page."""
    user_data = {"email": "abc123@gmail.com", "password": "password"}

    response = test_client.post("/login", data=user_data)
    assert response.status_code == 302
    yield test_client


def test_home_page(test_client):
    """Test the home page route."""
    response = test_client.get("/")
    assert response.status_code == 200


def test_login(test_client):
    """Test the home page route."""
    response = test_client.get("/login")
    assert response.status_code == 200


def test_register(test_client):
    """Tests register page."""
    user_data = {"email": "abc123@gmail.com", "password": "password"}

    response = test_client.post("/register", data=user_data)
    assert response.status_code == 302


def test_dashboard_page(client):
    """Test the dashboard page route."""
    response = client.get("/dashboard")
    assert response.status_code == 200


def test_dashboard_picture(client):
    """Tests picture taking functionality of dashboard."""
    with open("tests/test.jpg", "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    payload = {"image": f"data:image/jpeg;base64,{img_base64}"}

    response = client.post(
        "/dashboard", data=json.dumps(payload), content_type="application/json"
    )

    assert response.status_code == 200


def test_dashboard_upload(client):
    """Test uploading image to dashboard."""
    with open("tests/test.jpg", "rb") as img_file:
        data = {"image": (img_file, "test.jpg")}

        response = client.post(
            "/dashboard", data=data, content_type="multipart/form-data"
        )

    assert response.status_code == 200


def test_logout(client):
    """Tests logout."""
    response = client.get("/logout")
    assert response.status_code == 302
