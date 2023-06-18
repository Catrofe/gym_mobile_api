from sqlalchemy import select
from sqlalchemy.sql.expression import exists

from gym_project.api.financial.mapper import mapper_financial_output
from gym_project.api.financial.models import (
    ExtractFinancialRegister,
    FinancialOutput,
    FinancialRegister,
    FinancialUpdate,
)
from gym_project.infra.Entities.entities import (
    ExtractFinancial,
    Financial,
    PydanticExtractFinancial,
    PydanticFinancial,
    get_session_maker,
)


class FinancialRepository:
    def __init__(self) -> None:
        self.sessionmaker = get_session_maker()

    async def register_financial(self, body: FinancialRegister) -> PydanticFinancial:
        async with self.sessionmaker() as session:
            financial = Financial(**body.dict(exclude_unset=True))
            session.add(financial)
            await session.commit()
        return PydanticFinancial.from_orm(financial) if financial else None

    async def get_financial(self, id_financial: int) -> FinancialOutput | None:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Financial).where(Financial.id == id_financial)
            )
            result = query.scalar()
            return await mapper_financial_output(result) if result else None

    async def register_extract_financial(
        self, body: ExtractFinancialRegister
    ) -> PydanticExtractFinancial:
        async with self.sessionmaker() as session:
            extract_financial = ExtractFinancial(**body.dict(exclude_unset=True))
            session.add(extract_financial)
            await session.commit()
        return PydanticExtractFinancial.from_orm(extract_financial)

    async def verify_if_user_exists(self, user: int) -> bool:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select((exists(Financial))).filter((Financial.user == user))
            )
            return bool(query.scalar())

    async def update_financial(self, body: FinancialUpdate) -> FinancialOutput | None:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Financial).where(Financial.id == body.id)
            )
            financial = query.scalar()
            if financial is None:
                return None
            for key, value in body.dict(exclude_unset=True).items():
                setattr(financial, key, value)

            session.add(financial)
            await session.commit()
            return await mapper_financial_output(financial)

    async def get_financial_by_user(self, id_user: int) -> FinancialOutput | None:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Financial).where(Financial.user == id_user)
            )
            result = query.scalar()
            return await mapper_financial_output(result) if result else None
