import asyncio

import pytest
from fastapi.testclient import TestClient

from gym_project.api.auth.models import LoginAuthResponse
from gym_project.api.employee.models import PatchEmployeeActive, PatchEmployeeSuperuser
from gym_project.api.employee.repository import EmployeeRepository
from gym_project.app import app, startup_event

client = TestClient(app)


@pytest.fixture
def change_db_url():
    asyncio.run(startup_event())


@pytest.fixture
def create_employee(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
        "password": "1234ab1234",
    }
    client.post("/api/gym/employees/", json=request)


@pytest.fixture
def login_employee(create_employee) -> LoginAuthResponse:
    request_mock = PatchEmployeeActive(id=1, isActive=True)
    asyncio.run(EmployeeRepository().aprove_employee(request_mock))
    request_mock_superuser = PatchEmployeeSuperuser(id=1, isSuperuser=True)
    asyncio.run(EmployeeRepository().update_employee_admin(request_mock_superuser))

    response = client.post(
        "/api/gym/auth/",
        json={"login": "catrofe", "password": "1234ab1234", "typeUser": "employee"},
    )

    request_mock = PatchEmployeeActive(id=1, isActive=True)
    EmployeeRepository().aprove_employee(request_mock)

    if response.status_code == 200:
        return LoginAuthResponse(**response.json())


def test_create_employee_valid(change_db_url):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
        "password": "1234ab1234",
    }
    response = client.post("/api/gym/employees", json=request)

    assert response.status_code == 201


def test_create_employee_duplicated(create_employee):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
        "password": "1234ab1234",
    }
    response = client.post("/api/gym/employees", json=request)

    assert response.status_code == 400


def test_user_get_my_employee(login_employee):
    response = client.get(
        "/api/gym/employees/",
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    assert response.status_code == 200


def test_user_get_my_employee_error_token(login_employee):
    response = client.get(
        "/api/gym/employees/",
        headers={"Authorization": f"Bearer {login_employee.access_token}1"},
    )
    assert response.status_code == 401


def teste_get_by_id_employee(login_employee):
    response = client.get(
        "/api/gym/employees/1",
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    assert response.status_code == 200


def test_get_employee_by_id_404(login_employee):
    response = client.get(
        "/api/gym/employees/2",
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    assert response.status_code == 404


def test_employee_put_user_by_token(login_employee):
    json = {
        "fullName": "catrofinho",
        "email": "teste2@gmail.com",
        "phoneNumber": "21888888888",
    }
    response = client.put(
        "/api/gym/employees/",
        json=json,
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["fullName"] == "catrofinho"
    assert response.json()["email"] == "teste2@gmail.com"
    assert response.json()["phoneNumber"] == "21888888888"


def test_patch_change_password(login_employee):
    json = {
        "password": "123123123",
        "confirmPassword": "123123123",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
    }

    response = client.patch(
        "/api/gym/employees/password/",
        json=json,
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    assert response.status_code == 204


def test_patch_change_password_and_login(login_employee):
    json = {
        "password": "123123123",
        "confirmPassword": "123123123",
        "username": "catrofe",
        "cpf": "18313646705",
        "email": "teste@gmail.com",
        "phoneNumber": "21999999999",
    }

    client.patch(
        "/api/gym/employees/password",
        json=json,
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    response = client.post(
        "api/gym/auth/",
        json={
            "login": "teste@gmail.com",
            "password": "123123123",
            "typeUser": "employee",
        },
    )
    assert response.status_code == 200


def test_get_new_employees(login_employee):
    request = {
        "fullName": "Christian Lopes",
        "username": "catrofee",
        "cpf": "12345678908",
        "email": "teste@gmail.comm",
        "phoneNumber": "21999999998",
        "password": "1234ab1234",
    }
    client.post("/api/gym/employees", json=request)

    response2 = client.get(
        "/api/gym/employees/new-employees/",
        headers={"Authorization": f"Bearer {login_employee.access_token}"},
    )

    assert response2.status_code == 200
