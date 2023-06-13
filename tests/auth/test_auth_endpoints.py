import asyncio

import pytest
from fastapi.testclient import TestClient

from gym_project.api.auth.models import LoginAuthResponse
from gym_project.app import app, startup_event

client = TestClient(app)


@pytest.fixture
def change_db_url():
    asyncio.run(startup_event())


@pytest.fixture
def create_user(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
        "password": "1234ab1234",
    }
    client.post("/api/gym/users", json=request)


@pytest.fixture
def login_user(create_user) -> LoginAuthResponse:
    response = client.post(
        "/api/gym/auth/",
        json={"login": "catrofe", "password": "1234ab1234", "typeUser": "user"},
    )

    if response.status_code == 200:
        return LoginAuthResponse(**response.json())


def test_user_login_with_username(create_user):
    response = client.post(
        "/api/gym/auth/", json={"login": "catrofe", "password": "1234ab1234"}
    )

    assert response.status_code == 200


def test_user_login_with_cpf(create_user):
    response = client.post(
        "/api/gym/auth/", json={"login": "18313646705", "password": "1234ab1234"}
    )

    assert response.status_code == 200


def test_user_login_with_email(create_user):
    response = client.post(
        "/api/gym/auth/",
        json={"login": "teste@gmail.com", "password": "1234ab1234"},
    )

    assert response.status_code == 200


def test_user_login_with_phone_number(create_user):
    response = client.post(
        "/api/gym/auth/", json={"login": "21999999999", "password": "1234ab1234"}
    )

    assert response.status_code == 200


def test_user_login_not_found(create_user):
    response = client.post(
        "/api/gym/auth/", json={"login": "", "password": "1234ab1234"}
    )

    assert response.status_code == 404


def test_user_login_bad_request(create_user):
    response = client.post("/api/gym/auth/", json={"login": "catrofe", "password": ""})

    assert response.status_code == 400


def test_user_refresh_token_with_bearer(login_user):
    response = client.get(
        "/api/gym/auth/refresh/",
        headers={"Authorization": f"Bearer {login_user.refresh_token}"},
    )

    assert response.status_code == 200


def test_user_refresh_token_without_bearer(login_user):
    response = client.get(
        "/api/gym/auth/refresh/", headers={"Authorization": login_user.refresh_token}
    )

    assert response.status_code == 200


def test_user_refresh_token_error(login_user):
    response = client.get(
        "/api/gym/auth/refresh/", headers={"Authorization": login_user.access_token}
    )

    assert response.status_code == 401
