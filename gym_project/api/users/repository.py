from fastapi import status
from sqlalchemy import select

from gym_project.api.users.models import UserEdit, UserLogin, UserRegister
from gym_project.infra.Entities.entities import PydanticUser, User, get_session_maker
from gym_project.utils.erros_util import RaiseErrorGym


class UserRepository:
    def __init__(self) -> None:
        self.sessionmaker = get_session_maker()

    async def user_is_valid(self, user: UserRegister) -> bool:
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
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))

    async def user_is_valid_to_edit(self, user: UserEdit) -> bool:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                    select(
                        User.username, User.cpf, User.email, User.phoneNumber
                    ).filter(
                        (User.email == user.email)
                        | (User.phoneNumber == user.phoneNumber)
                    )
                )
                result = query.scalar()
                if result:
                    return False
                return True
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))

    async def register_user(self, user_request: UserRegister) -> PydanticUser:
        try:
            async with self.sessionmaker() as session:
                user = User(**user_request.dict())
                session.add(user)
                await session.commit()
                return PydanticUser.from_orm(user)
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))

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
                result = query.scalar()
                if result:
                    return PydanticUser.from_orm(result)
                return None
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))

    async def get_user(self, id_user: int) -> PydanticUser | None:
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(select(User).filter(User.id == id_user))
                result = query.scalar()
                if result:
                    return PydanticUser.from_orm(result)
                return None
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))

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
            print("repo")
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(error))
