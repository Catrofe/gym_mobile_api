from fastapi import APIRouter, Depends, Request, status

from gym_project.api.auth.models import LoginToken
from gym_project.api.employee.models import (
    EmployeeEdit,
    EmployeeForgotPassword,
    EmployeeOutput,
    EmployeeRegister,
    PatchEmployeeActive,
    PatchEmployeeSuperuser,
)
from gym_project.api.employee.service import EmployeeService
from gym_project.utils.auth_utils_poc import is_admin, is_employee, jwt_authorization

service = EmployeeService()

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeOutput)
async def create_employee(body: EmployeeRegister, request: Request) -> EmployeeOutput:
    return await service.register_employee(body, request)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_employee)],
    response_model=EmployeeOutput,
)
async def get_employee(request: Request) -> EmployeeOutput:
    employee = LoginToken(**request.state.user)
    return await service.get_employee(employee, request)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_employee)],
    response_model=EmployeeOutput,
)
async def get_employee_by_id(id: int, request: Request) -> EmployeeOutput:
    return await service.get_employee_by_id(id, request)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_employee)],
    response_model=EmployeeOutput,
)
async def update_employee(body: EmployeeEdit, request: Request) -> EmployeeOutput:
    employee = LoginToken(**request.state.user)
    return await service.update_employee(employee, body, request)


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee_password(
    body: EmployeeForgotPassword, request: Request
) -> None:
    await service.update_password(body, request)


@router.get(
    "/new-employees/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_admin)],
    response_model=list[EmployeeOutput],
)
async def get_all_new_employee(request: Request) -> list[EmployeeOutput]:
    return await service.get_all_employees_no_active(request)


@router.patch(
    "/activity/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_admin)],
    response_model=EmployeeOutput,
)
async def aprove_employee(
    body: PatchEmployeeActive, request: Request
) -> EmployeeOutput:
    return await service.aprove_employee(body, request)


@router.patch(
    "/admin/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_admin)],
    response_model=EmployeeOutput,
)
async def update_employee_admin(
    body: PatchEmployeeSuperuser, request: Request
) -> EmployeeOutput:
    return await service.update_employee_admin(body, request)
