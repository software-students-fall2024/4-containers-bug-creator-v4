import pytest
import base64
from unittest.mock import patch, MagicMock
from app import app
from werkzeug.security import generate_password_hash


@pytest.fixture(name="guest")
def fixture_guest():
    """Mock guest fixture"""
    with app.test_client() as guest:
        yield guest


@pytest.fixture(name="client")
def fixture_client():
    """Mock client fixture"""
    with app.test_client() as client:
        with app.app_context():
            with client.session_transaction() as session:
                session["user"] = "abc123@gmail.com"
        yield client


def get_login(guest):
    """Test the home page route."""
    response = guest.get("/login")
    assert response.status_code == 200


@patch(
    "app.models.Database.find_user",
    return_value={
        "email": "abc123@gmail.com",
        "password": generate_password_hash("test"),
    },
)
def test_login(mock, guest):
    """Tests logging in."""
    form_data = {"email": "abc123@gmail.com", "password": "test"}
    response = guest.post("/login", data=form_data)
    assert response.status_code == 302


def test_logout(client):
    """Tests logging out."""
    response = client.get("/logout")
    assert response.status_code == 302


def get_register(guest):
    """Tests register page."""
    response = guest.get("/register")
    assert response.status_code == 302


@patch("app.models.Database.find_user", return_value=None)
@patch("app.models.Database.add_user")
def test_register(mock_add_user, mock_find_user, guest):
    """Tests user registration."""
    form_data = {"email": "newuser@gmail.com", "password": "password"}

    response = guest.post("/register", data=form_data)
    assert response.status_code == 302


@patch("app.models.Database.get_latest_results", return_value=[])
def test_home_page(mock, client):
    """Test the home page route."""
    response = client.get("/")
    assert response.status_code == 200


def test_upload(client):
    """Test upload page route."""
    response = client.get("/upload")
    assert response.status_code == 200


@patch(
    "app.models.Database.save_picture",
    return_value={"image_url": "url", "emotion": {}},
)
def test_upload(mock, client):
    """
    Test uploading picture files.
    """
    mock_image_data = MagicMock()
    mock_image_data.read.return_value = b"mock_image_data"

    response = client.post(
        "/upload",
        data={"image": mock_image_data},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200


@patch("app.models.Database.get_latest_results", return_value=[])
def test_camera(mock, client):
    """Test camera page route."""
    response = client.get("/camera")
    assert response.status_code == 200


@patch(
    "app.models.Database.save_picture", return_value={"image_url": "url", "emotion": {}}
)
def test_camera_post(mock, client):
    """
    Tests camera functionality.
    """

    mock_image_data = base64.b64encode(b"test_image_data").decode("utf-8")
    mock_payload = {"image": f"data:image/png;base64,{mock_image_data}"}

    response = client.post("/camera", json=mock_payload)

    assert response.status_code == 200
