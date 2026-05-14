import pytest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)


test_user = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "strongpassword123",
    "telephone": "123456789"
}

def test_register_user():
    """Тест успешной регистрации"""
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert "id" in data

def test_register_duplicate_email():
    """Тест ошибки при регистрации существующего email"""
    client.post("/auth/register", json=test_user)
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_success():
    """Тест успешного входа и получения токена"""
    client.post("/auth/register", json=test_user)
    
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """Тест входа с неправильным паролем"""
    login_data = {
        "username": test_user["email"],
        "password": "wrong_password"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"