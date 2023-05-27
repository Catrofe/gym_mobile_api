import bcrypt
from fastapi import Request, status

from gym_project.api.auth.models import LoginToken
from gym_project.api.employee.models import (
    EmployeeEdit,
    EmployeeForgotPassword,
    EmployeeOutput,
    EmployeeRegister,
    PatchEmployeeActive,
    PatchEmployeeSuperuser,
)
from gym_project.api.employee.repository import EmployeeRepository
from gym_project.utils.erros_util import RaiseErrorGym


class EmployeeService:
    def __init__(self) -> None:
        self._repository = EmployeeRepository()

    async def register_employee(
        self, body: EmployeeRegister, request: Request
    ) -> EmployeeOutput:
        if not await self._repository.employee_is_valid(body):
            body.password = await self.encode_password(body.password)
            employee = await self._repository.register_employee(body)
            return EmployeeOutput(**employee.dict())

        raise RaiseErrorGym(
            request, status.HTTP_400_BAD_REQUEST, "Employee already exists"
        )

    @staticmethod
    async def encode_password(raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()

    async def get_employee(self, body: LoginToken, request: Request) -> EmployeeOutput:
        employee = await self._repository.get_employee(body.id)
        if employee:
            return EmployeeOutput(**employee.dict())

        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "Employee not found")

    async def get_employee_by_id(self, body: int, request: Request) -> EmployeeOutput:
        employee = await self._repository.get_employee(body)
        if employee:
            return EmployeeOutput(**employee.dict())

        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "Employee not found")

    async def update_employee(
        self, employee_token: LoginToken, body: EmployeeEdit, request: Request
    ) -> EmployeeOutput:
        if not await self._repository.employee_is_valid_to_edit(body):
            if body.password:
                body.password = await self.encode_password(body.password)
            employee = await self._repository.update_employee(employee_token.id, body)
            if employee:
                return EmployeeOutput(**employee.dict())

        raise RaiseErrorGym(
            request, status.HTTP_400_BAD_REQUEST, "Employee not valid to edit"
        )

    async def update_password(
        self, body: EmployeeForgotPassword, request: Request
    ) -> bool:
        if await self._repository.verify_if_is_employee(body):
            if body.password == body.confirmPassword:
                body.password = await self.encode_password(body.password)
                await self._repository.update_password(body)
                return True
            raise RaiseErrorGym(
                request, status.HTTP_400_BAD_REQUEST, "Passwords do not match"
            )
        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "Employee not found")

    async def get_all_employees_no_active(
        self, request: Request
    ) -> list[EmployeeOutput]:
        employees = await self._repository.get_all_employees_no_active()
        if employees:
            return [EmployeeOutput(**employee.dict()) for employee in employees]
        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "Employees not found")

    async def aprove_employee(
        self, body: PatchEmployeeActive, request: Request
    ) -> EmployeeOutput:
        employee = await self._repository.aprove_employee(body)
        if employee:
            return EmployeeOutput(**employee.dict())
        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "Employee not found")

    async def update_employee_admin(
        self, body: PatchEmployeeSuperuser, request: Request
    ) -> EmployeeOutput:
        employee = await self._repository.update_employee_admin(body)
        if employee:
            return EmployeeOutput(**employee.dict())
        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "Employee not found")
