from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

async def setup_db(db_url: str) -> None:
    engine = create_async_engine(
        db_url,
        echo=False,
    )
    sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150))
    username = Column(String(50), unique=True, index=True)
    cpf = Column(String(11), unique=True, index=True)
    email = Column(String(70), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.now())