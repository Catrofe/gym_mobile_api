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


def test_create_user_valid(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
        "password": "1234ab1234",
    }
    response = client.post("/api/gym/users", json=request)

    assert response.status_code == 201


def test_create_user_bad_request(create_user):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
        "password": "1234ab1234",
    }

    response = client.post("/api/gym/users", json=request)

    assert response.status_code == 400


def test_user_get_my_user(login_user):
    response = client.get(
        "/api/gym/users/",
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )

    assert response.status_code == 200


def test_user_get_my_user_error_token(login_user):
    response = client.get(
        "/api/gym/users/", headers={"Authorization": login_user.refresh_token}
    )

    assert response.status_code == 401


def test_get_user_by_id(login_user):
    response = client.get(
        "/api/gym/users/1",
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )

    assert response.status_code == 200


def test_get_user_by_id_404(login_user):
    response = client.get(
        "/api/gym/users/3",
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )

    assert response.status_code == 404


def test_get_user_by_id_error_token(login_user):
    response = client.get(
        "/api/gym/users/1", headers={"Authorization": login_user.refresh_token}
    )

    assert response.status_code == 401


def test_put_user_by_token(login_user):
    json = {
        "fullName": "catrofinho",
        "email": "teste2@gmail.com",
        "phoneNumber": "21888888888",
    }

    response = client.put(
        "/api/gym/users/",
        json=json,
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["fullName"] == "catrofinho"
    assert response.json()["email"] == "teste2@gmail.com"
    assert response.json()["phoneNumber"] == "21888888888"


def test_put_user_by_token_and_login(login_user):
    json = {"email": "teste2@gmail.com", "password": "123123123"}

    client.put(
        "/api/gym/users/",
        json=json,
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )

    response = client.post(
        "api/gym/auth/",
        json={"login": "teste2@gmail.com", "password": "123123123", "typeUser": "user"},
    )
    assert response.status_code == 200


def test_patch_change_password(login_user):
    json = {
        "password": "123123123",
        "confirmPassword": "123123123",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
    }

    response = client.patch(
        "/api/gym/users/password",
        json=json,
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )
    assert response.status_code == 204


def test_patch_change_password_and_login(login_user):
    json = {
        "password": "123123123",
        "confirmPassword": "123123123",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
    }

    client.patch(
        "/api/gym/users/password",
        json=json,
        headers={"Authorization": f"Bearer {login_user.access_token}"},
    )

    response = client.post(
        "api/gym/auth/",
        json={"login": "teste@gmail.com", "password": "123123123", "typeUser": "user"},
    )
    assert response.status_code == 200
