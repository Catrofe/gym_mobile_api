import asyncio

import pytest
from fastapi.testclient import TestClient

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
        "phoneNumber": "21974900682",
        "password": "1234ab1234",
    }
    client.post("/api/gym/users", json=request)


def test_create_user_valid(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21974900682",
        "password": "1234ab1234",
    }
    response = client.post("/api/gym/users", json=request)

    assert response.status_code == 201


def test_create_user_bad_request(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21974900682",
        "password": "1234ab1234",
    }

    for i in range(2):
        response = client.post("/api/gym/users", json=request)

    assert response.status_code == 400


def test_user_login_with_username(create_user):
    response = client.post(
        "/api/gym/users/login", json={"login": "catrofe", "password": "1234ab1234"}
    )

    assert response.status_code == 200


def test_user_login_with_cpf(create_user):
    response = client.post(
        "/api/gym/users/login", json={"login": "18313646705", "password": "1234ab1234"}
    )

    assert response.status_code == 200


def test_user_login_with_email(create_user):
    response = client.post(
        "/api/gym/users/login",
        json={"login": "teste@gmail.com", "password": "1234ab1234"},
    )

    assert response.status_code == 200


def test_user_login_with_phone_number(create_user):
    response = client.post(
        "/api/gym/users/login", json={"login": "21974900682", "password": "1234ab1234"}
    )

    assert response.status_code == 200


def test_user_login_not_found(create_user):
    response = client.post(
        "/api/gym/users/login", json={"login": "", "password": "1234ab1234"}
    )

    assert response.status_code == 404


def test_user_login_bad_request(create_user):
    response = client.post(
        "/api/gym/users/login", json={"login": "catrofe", "password": ""}
    )

    assert response.status_code == 400
