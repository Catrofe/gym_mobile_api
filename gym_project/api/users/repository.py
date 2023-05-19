from fastapi import status
from sqlalchemy import select

from gym_project.infra.Entities.entities import PydanticUser, User, get_session_maker
from gym_project.utils.erros_util import RaiseErrorGym


class UserRepository:
    def __init__(self):
        self.sessionmaker = get_session_maker()

    async def user_is_valid(self, user):
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select(
                        User.username, User.cpf, User.email, User.phoneNumber
                    ).filter(
                        (User.username == user.username)
                        | (User.cpf == user.cpf)
                        | (User.email == user.email)
                        | (User.phoneNumber == user.phoneNumber)
                    )
                )
                result = query.scalar()
                if result:
                    return False
                return True
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, error)

    async def register_user(self, user):
        try:
            async with self.sessionmaker() as session:
                user = User(**user.dict())
                session.add(user)
                await session.commit()
                return PydanticUser.from_orm(user)
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, error)

    async def login_user(self, user):
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select(User).filter(
                        (User.username == user.login)
                        | (User.cpf == user.login)
                        | (User.email == user.login)
                        | (User.phoneNumber == user.login)
                    )
                )
                result = query.scalar()
                if result:
                    return PydanticUser.from_orm(result)
                return None
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, error)
