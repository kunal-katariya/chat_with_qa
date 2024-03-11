import pytest
import requests

BASE_URL = "http://localhost:7000"

@pytest.fixture
def session_user():
    data = {"user_email": "final@final.com", "password": "final"}
    response = requests.post(f"{BASE_URL}/login", json=data)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        pytest.fail("Login failed")

@pytest.mark.parametrize("user_email, password", [("kunal@yash.com", "kunal123"), ("ram@gmail.com", "string123")])
def test_user_login_success(user_email, password):
    data = {"user_email": user_email, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 200

@pytest.mark.parametrize("user_email, password", [("kunal@yash.com", "string123"), ("ram@gmail.com", "kunal123")])
def test_user_login_failure(user_email, password):
    data = {"user_email": user_email, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=data)
    assert response.status_code == 401

def test_read_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200

def test_read_user_success(session_user):
    user_id = session_user["id"]
    response = requests.get(f"{BASE_URL}/user/{user_id}")
    assert response.status_code == 200

@pytest.mark.parametrize("user_id", [1, 2, 9])
def test_read_user_not_found(user_id):
    user_id = user_id
    response = requests.get(f"{BASE_URL}/user/{user_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_success():
    user_data = {"name": "newuser", "email": "newuser@example.com", "password": "password123", "user_type": "normal_user"}
    response = requests.post(f"{BASE_URL}/create_user", json=user_data)
    assert response.status_code == 201

def test_create_user_existing_email():
    user_data = {"name": "newuser", "email": "newuser@example.com", "password": "password123", "user_type": "normal_user"}
    response = requests.post(f"{BASE_URL}/create_user", json=user_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email is already registered"}

def test_create_user_missing_fields():
    user_data = {"email": "newuser3@example.com"}
    response = requests.post(f"{BASE_URL}/create_user", json=user_data)
    assert response.status_code == 422

def test_delete_user_success(session_user):
    user_id = session_user["id"]
    response = requests.delete(f"{BASE_URL}/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == "User deleted successfully"

def test_delete_nonexistent_user():
    nonexistent_id = 12345
    response = requests.delete(f"{BASE_URL}/user/{nonexistent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
