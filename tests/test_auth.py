import pytest
from app import app, users

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# очищаем базу перед тестами
@pytest.fixture(autouse=True)
def clear_db():
    users.delete_many({})

# тест регистрации
def test_register(client):
    response = client.post("/register", json={
        "email": "test@mail.com",
        "password": "1234"
    })
    assert response.status_code == 201


# тест логина (с bcrypt!)
def test_login_success(client):
    client.post("/register", json={
        "email": "test@mail.com",
        "password": "1234"
    })

    response = client.post("/login", json={
        "email": "test@mail.com",
        "password": "1234"
    })

    assert response.status_code == 200


# тест неверного логина
def test_login_fail(client):
    response = client.post("/login", json={
        "email": "wrong@mail.com",
        "password": "1234"
    })

    assert response.status_code == 401