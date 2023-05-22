from fastapi import status
from sqlalchemy import select, update
from sqlalchemy.sql.expression import exists

from gym_project.api.users.models import (
    UserEdit,
    UserForgotPassword,
    UserLogin,
    UserRegister,
)
from gym_project.infra.Entities.entities import PydanticUser, User, get_session_maker
from gym_project.utils.erros_util import RaiseErrorGym


class UserRepository:
    def __init__(self) -> None:
        self.sessionmaker = get_session_maker()

    async def user_is_valid(self, user: UserRegister) -> bool:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select((exists(User))).filter(
                        (User.username == user.username)
                        | (User.cpf == user.cpf)
                        | (User.email == user.email)
                        | (User.phoneNumber == user.phoneNumber)
                    )
                )
                return bool(query.scalar())
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def user_is_valid_to_edit(self, user: UserEdit) -> bool:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select(
                        (exists(User)).filter(
                            (User.email == user.email)
                            | (User.phoneNumber == user.phoneNumber)
                        )
                    )
                )
                return bool(query.scalar())
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def register_user(self, user_request: UserRegister) -> PydanticUser:
        try:
            async with self.sessionmaker() as session:
                user = User(**user_request.dict())
                session.add(user)
                await session.commit()
                return PydanticUser.from_orm(user)
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def login_user(self, user: UserLogin) -> PydanticUser | None:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select(User)
                    .where(User.isActive)
                    .filter(
                        (User.username == user.login)
                        | (User.cpf == user.login)
                        | (User.email == user.login)
                        | (User.phoneNumber == user.login)
                    )
                )
                return (
                    PydanticUser.from_orm(result)
                    if (result := query.scalar())
                    else None
                )
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def get_user(self, id_user: int) -> PydanticUser | None:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(select(User).filter(User.id == id_user))
                return (
                    PydanticUser.from_orm(result)
                    if (result := query.scalar())
                    else None
                )
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def update_user(self, user_id: int, user_request: UserEdit) -> PydanticUser:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(select(User).filter(User.id == user_id))
                result = query.scalar()

                for attr, value in user_request.dict().items():
                    if value:
                        setattr(result, attr, value)

                session.add(result)
                await session.commit()
                return PydanticUser.from_orm(result)
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def verify_if_is_user(self, user_request: UserForgotPassword) -> bool:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select(exists(User)).where(
                        User.username == user_request.username,
                        User.email == user_request.email,
                        User.cpf == user_request.cpf,
                        User.phoneNumber == user_request.phoneNumber,
                        User.isActive,
                    )
                )
            return bool(query.scalar())
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error

    async def update_password(self, user_request: UserForgotPassword) -> None:
        try:
            async with self.sessionmaker() as session:
                await session.execute(
                    update(User)
                    .where(User.email == user_request.email)
                    .values(password=user_request.password)
                )
                await session.commit()
        except Exception as error:
            raise RaiseErrorGym(
                status.HTTP_500_INTERNAL_SERVER_ERROR, str(error)
            ) from error
