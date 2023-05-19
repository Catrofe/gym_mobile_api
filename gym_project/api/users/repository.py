from gym_project.infra.Entities.entities import User
from sqlalchemy import select, update
from gym_project.utils.erros_util import RaiseErrorGym
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker



class UserRepository:

    def __init__(self):
        engine = create_async_engine(
            "sqlite+aiosqlite:///db.db",
            echo=False,
        )
        self.sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def user_is_valid(self, user):
        try:
            async with self.sessionmaker() as session:
                query = await session.execute(
                   select(User.username, User.cpf, User.email, User.phoneNumber).filter(
                        (User.username == user.username) |
                        (User.cpf == user.cpf) |
                        (User.email == user.email) |
                        (User.phoneNumber == user.phoneNumber)
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
                return user
        except Exception as error:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, error)