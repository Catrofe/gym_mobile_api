from sqlalchemy import select

from gym_project.api.auth.models import LoginAuth
from gym_project.infra.Entities.entities import (
    Employee,
    PydanticEmployee,
    PydanticUser,
    User,
    get_session_maker,
)


class AuthRepository:
    def __init__(self) -> None:
        self.sessionmaker = get_session_maker()

    async def login_user_auth(self, body: LoginAuth) -> PydanticUser:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(User)
                .where(User.isActive)
                .filter(
                    (User.username == body.login)
                    | (User.cpf == body.login)
                    | (User.email == body.login)
                    | (User.phoneNumber == body.login)
                )
            )
        return PydanticUser.from_orm(result) if (result := query.scalar()) else None

    async def login_employee_auth(self, body: LoginAuth) -> PydanticEmployee:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Employee)
                .where(Employee.isActive)
                .filter(
                    (Employee.username == body.login)
                    | (Employee.cpf == body.login)
                    | (Employee.email == body.login)
                    | (Employee.phoneNumber == body.login)
                )
            )
        return PydanticEmployee.from_orm(result) if (result := query.scalar()) else None

    async def get_employee_by_id(self, id_user: int) -> PydanticEmployee:
        async with self.sessionmaker() as session:
            query = await session.execute(
                select(Employee).where(Employee.id == id_user)
            )
        return PydanticEmployee.from_orm(result) if (result := query.scalar()) else None

    async def get_user_by_id(self, id_user: int) -> PydanticEmployee:
        async with self.sessionmaker() as session:
            query = await session.execute(select(User).where(User.id == id_user))
        return PydanticEmployee.from_orm(result) if (result := query.scalar()) else None
