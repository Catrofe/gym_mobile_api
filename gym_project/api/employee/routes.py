from fastapi import APIRouter, Depends, Request, status

from gym_project.api.employee.models import (
    EmployeeAuth,
    EmployeeEdit,
    EmployeeForgotPassword,
    EmployeeLogin,
    EmployeeOutput,
    EmployeeRegister,
    PatchEmployeeActive,
    PatchEmployeeSuperuser,
)
from gym_project.api.employee.service import EmployeeService
from gym_project.utils.auth_utils import (
    EmployeeToken,
    decode_refresh_token_employee,
    decode_token_jwt,
    decode_token_jwt_employee,
)

service = EmployeeService()

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=EmployeeOutput)
async def create_employee(body: EmployeeRegister, request: Request) -> EmployeeOutput:
    return await service.register_employee(body, request)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=EmployeeAuth)
async def login_employee(body: EmployeeLogin, request: Request) -> EmployeeAuth:
    return await service.login_employee(body, request)


@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=EmployeeAuth)
async def refresh_token(
    employee: EmployeeToken = Depends(decode_refresh_token_employee),
) -> EmployeeAuth:
    return await service.generate_auth_employee(employee)


@router.get("/", status_code=status.HTTP_200_OK, response_model=EmployeeOutput)
async def get_employee(
    request: Request, employee: EmployeeToken = Depends(decode_token_jwt_employee)
) -> EmployeeOutput:
    return await service.get_employee(employee, request)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=EmployeeOutput)
async def get_employee_by_id(id: int, request: Request) -> EmployeeOutput:
    await decode_token_jwt(
        request, authorization=str(request.headers.get("Authorization"))
    )
    return await service.get_employee_by_id(id, request)


@router.put("/", status_code=status.HTTP_200_OK, response_model=EmployeeOutput)
async def update_employee(
    body: EmployeeEdit,
    request: Request,
    employee: EmployeeToken = Depends(decode_token_jwt_employee),
) -> EmployeeOutput:
    return await service.update_employee(employee, body, request)


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_employee_password(
    body: EmployeeForgotPassword, request: Request
) -> None:
    await service.update_password(body, request)


@router.get(
    "/new-employees/",
    status_code=status.HTTP_200_OK,
    response_model=list[EmployeeOutput],
)
async def get_all_new_employee(request: Request) -> list[EmployeeOutput]:
    return await service.get_all_employees_no_active(request)


@router.patch(
    "/activity/", status_code=status.HTTP_200_OK, response_model=EmployeeOutput
)
async def aprove_employee(
    body: PatchEmployeeActive, request: Request
) -> EmployeeOutput:
    await decode_token_jwt_employee(
        request, authorization=str(request.headers.get("Authorization"))
    )
    return await service.aprove_employee(body, request)


@router.patch("/admin/", status_code=status.HTTP_200_OK, response_model=EmployeeOutput)
async def update_employee_admin(
    body: PatchEmployeeSuperuser, request: Request
) -> EmployeeOutput:
    await decode_token_jwt_employee(
        request, authorization=str(request.headers.get("Authorization"))
    )
    return await service.update_employee_admin(body, request)
