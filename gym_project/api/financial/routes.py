from fastapi import APIRouter, Request, status

from gym_project.api.financial.models import (
    ExtractFinancialOutput,
    ExtractFinancialRegister,
    FinancialOutput,
    FinancialRegister,
    FinancialUpdate,
)
from gym_project.api.financial.service import FinancialService

service = FinancialService()

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=FinancialOutput)
async def create_financial(
    body: FinancialRegister, request: Request
) -> FinancialOutput:
    return await service.register_financial(body, request)


@router.get(
    "/{id_financial}", status_code=status.HTTP_200_OK, response_model=FinancialOutput
)
async def get_financial(id_financial: int, request: Request) -> FinancialOutput:
    return await service.get_financial(id_financial, request)


@router.get(
    "user/{id_user}", status_code=status.HTTP_200_OK, response_model=FinancialOutput
)
async def get_financial_by_user(id_user: int, request: Request) -> FinancialOutput:
    return await service.get_financial_by_user(id_user, request)


@router.put("/", status_code=status.HTTP_200_OK, response_model=FinancialOutput)
async def update_financial(body: FinancialUpdate, request: Request) -> FinancialOutput:
    return await service.update_financial(body, request)


@router.post(
    "/extract",
    status_code=status.HTTP_201_CREATED,
    response_model=ExtractFinancialOutput,
)
async def create_extract_financial(
    body: ExtractFinancialRegister, request: Request
) -> ExtractFinancialOutput:
    return await service.register_extract_financial(body, request)
