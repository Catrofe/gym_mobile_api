from fastapi import Request, status

from gym_project.api.employee.service import EmployeeService
from gym_project.api.financial.models import (
    ExtractFinancialOutput,
    ExtractFinancialRegister,
    FinancialOutput,
    FinancialRegister,
    FinancialUpdate,
)
from gym_project.api.financial.repository import FinancialRepository
from gym_project.api.users.service import UserService
from gym_project.utils.erros_util import RaiseErrorGym


class FinancialService:
    def __init__(self) -> None:
        self._repository = FinancialRepository()
        self._service_user = UserService()
        self._service_employee = EmployeeService()

    async def register_financial(
        self, body: FinancialRegister, request: Request
    ) -> FinancialOutput:
        if await self._repository.verify_if_user_exists(body.user):
            raise RaiseErrorGym(
                request, status.HTTP_400_BAD_REQUEST, "Financial already exists"
            )

        await self._service_user.get_user_by_id(body.user, request)

        financial = await self._repository.register_financial(body)
        if financial:
            return FinancialOutput(**financial.dict())

        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "Employee not found")

    async def get_financial(
        self, id_financial: int, request: Request
    ) -> FinancialOutput:
        financial = await self._repository.get_financial(id_financial)
        if financial:
            return financial
        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "Financial not found")

    async def register_extract_financial(
        self, body: ExtractFinancialRegister, request: Request
    ) -> ExtractFinancialOutput:
        extract_body = ExtractFinancialRegister(
            idFinancial=body.idFinancial, idEmployee=body.idEmployee, value=body.value
        )
        extract_financial = await self._repository.register_extract_financial(
            extract_body
        )
        await self.update_financial(
            FinancialUpdate(
                id=body.idFinancial,
                methodPayment=body.methodPayment,
                dtMaturity=body.dtMaturity,
            ),
            request,
        )
        if extract_financial:
            return ExtractFinancialOutput(**extract_financial.dict())
        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "Financial not found")

    async def update_financial(
        self, body: FinancialUpdate, request: Request
    ) -> FinancialOutput:
        financial = await self._repository.get_financial(body.id)
        if financial:
            financial_updated = await self._repository.update_financial(body)
            if financial_updated:
                return FinancialOutput(**financial.dict())
        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "Financial not found")

    async def get_financial_by_user(
        self, id_user: int, request: Request
    ) -> FinancialOutput:
        financial = await self._repository.get_financial_by_user(id_user)
        if financial:
            return financial
        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "User not found")
