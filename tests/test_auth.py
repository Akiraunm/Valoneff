import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import bcrypt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app, users

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# -------------------------------
# Тест регистрации с моками
# -------------------------------
@patch("app.users")
def test_register(mock_users, client):
    # имитация вставки пользователя в базу
    mock_users.find_one.return_value = None  # пользователь ещё не существует
    mock_users.insert_one.return_value = MagicMock(inserted_id="123")

    response = client.post("/register", json={
        "email": "test@mail.com",
        "password": "1234"
    })

    assert response.status_code == 201
    args, kwargs = mock_users.insert_one.call_args
    assert args[0]["email"] == "test@mail.com"
    assert "password" in args[0]  # пароль захеширован

# -------------------------------
# Тест успешного логина с моками
# -------------------------------
@patch("app.users")
def test_login_success(mock_users, client):
    # создаём мок пользователя с динамическим хешем
    password = "1234".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    mock_users.find_one.return_value = {"email": "test@mail.com", "password": hashed_password}

    response = client.post("/login", json={
        "email": "test@mail.com",
        "password": "1234"
    })

    assert response.status_code == 200
    mock_users.find_one.assert_called_once_with({"email": "test@mail.com"})

# -------------------------------
# Тест неудачного логина с моками
# -------------------------------
@patch("app.users")
def test_login_fail(mock_users, client):
    # имитация, что пользователя нет
    mock_users.find_one.return_value = None

    response = client.post("/login", json={
        "email": "wrong@mail.com",
        "password": "1234"
    })

    assert response.status_code == 401
    mock_users.find_one.assert_called_once_with({"email": "wrong@mail.com"})
