from __future__ import annotations

from datetime import datetime

from pydantic_sqlalchemy import sqlalchemy_to_pydantic  # type: ignore
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from gym_project.utils.settings import Settings

settings = Settings()

Base = declarative_base()


def get_session_maker() -> sessionmaker[AsyncSession]:
    url = settings.db_prod if settings.ambiente is None else settings.db_test
    engine = create_async_engine(
        url,
        echo=False,
    )
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def create_database() -> None:
    url = settings.db_prod if settings.ambiente is None else settings.db_test
    engine = create_async_engine(
        url,
        echo=False,
    )
    if settings.ambiente == "TEST":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String(150))
    username = Column(String(50), unique=True, index=True)
    cpf = Column(String(11), unique=True, index=True)
    email = Column(String(70), unique=True, index=True)
    phoneNumber = Column(String(15), unique=True)
    password = Column(String(255))
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.now())


PydanticUser = sqlalchemy_to_pydantic(User)
