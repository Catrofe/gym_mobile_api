from __future__ import annotations

from datetime import datetime
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class GymDatabase:

    def __init__(self) -> None:
        self.sessionmaker = sessionmaker

    async def setup_db(self) -> None:
        engine = create_async_engine(
            "sqlite+aiosqlite:///db.db",
            echo=False,
        )
        self.sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def return_sessionmaker(self) -> AsyncSession:
        return self.sessionmaker()

DATABASE = GymDatabase()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullName = Column(String(150))
    username = Column(String(50), unique=True, index=True)
    cpf = Column(String(11), unique=True, index=True)
    email = Column(String(70), unique=True, index=True)
    phoneNumber = Column(String(15), unique=True)
    password = Column(String(255))
    isActive = Column(Boolean, default=False)
    isSuperuser = Column(Boolean, default=False)
    createdAt = Column(DateTime, default=datetime.now())
    updatedAt = Column(DateTime, onupdate=datetime.now())

PydanticUser = sqlalchemy_to_pydantic(User)