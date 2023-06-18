from gym_project.api.financial.models import ExtractFinancialOutput, FinancialOutput
from gym_project.infra.Entities.entities import Financial


async def mapper_financial_output(financial: Financial) -> FinancialOutput:
    extract_financial = []
    if financial.extractFinancial is None:
        return FinancialOutput(
            id=financial.id,
            user=financial.user,
            methodPayment=financial.methodPayment,
            dtMaturity=financial.dtMaturity,
            dtFirstPayment=financial.dtFirstPayment,
            extractFinancial=[],
            createdAt=financial.createdAt,
            updatedAt=financial.updatedAt,
        )

    for extract in financial.extractFinancial:
        item = ExtractFinancialOutput(
            id=extract.id,
            value=extract.value,
            idFinancial=extract.idFinancial,
            idEmployee=extract.idEmployee,
            createdAt=extract.createdAt,
        )
        extract_financial.append(item)
    return FinancialOutput(
        id=financial.id,  # type: ignore
        user=financial.user,  # type: ignore
        methodPayment=financial.methodPayment,
        dtMaturity=financial.dtMaturity,
        dtFirstPayment=financial.dtFirstPayment,
        extractFinancial=extract_financial,
        createdAt=financial.createdAt,  # type: ignore
        updatedAt=financial.updatedAt,
    )
