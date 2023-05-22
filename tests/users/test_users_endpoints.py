import asyncio

import pytest
from fastapi.testclient import TestClient

from gym_project.app import app, startup_event

client = TestClient(app)


@pytest.fixture
def change_db_url():
    asyncio.run(startup_event())


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


def test_create_user_conflict(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21974900682",
        "password": "1234ab1234",
    }

    client.post("/api/gym/users", json=request)
    response = client.post("/api/gym/users", json=request)

    assert response.status_code == 400
