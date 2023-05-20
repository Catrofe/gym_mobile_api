import datetime

import jwt
from fastapi import Header, HTTPException
from pydantic import BaseModel

from gym_project.infra.Entities.entities import User
from gym_project.utils.settings import Settings

settings: Settings = Settings()


class UserToken(BaseModel):
    id: int
    isSuperuser: bool
    isActive: bool
    createdAt: str


async def decode_token_jwt(authorization: str = Header()) -> UserToken:
    try:
        token = jwt.decode(
            authorization,
            settings.secret_key,
            leeway=datetime.timedelta(seconds=settings.secret_expires),
            algorithms=["HS256"],
        )
        return UserToken(
            id=token["id"],
            is_superuser=token["is_superuser"],
            is_active=token["is_active"],
            created_at=token["created_at"],
        )

    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(401, "INVALID_SIGNATURE")

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, "TOKEN_HAS_EXPIRED")

    except jwt.exceptions.DecodeError:
        raise HTTPException(401, "TOKEN_INVALID")


async def encode_token_jwt(user: User) -> str:
    return jwt.encode(
        {
            "id": user.id,
            "is_superuser": user.isSuperuser,
            "is_active": user.isActive,
            "created_at": str(user.createdAt),
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=settings.secret_expires),
        },
        settings.secret_key,
        algorithm="HS256",
    )


async def generate_refresh_token(user: User) -> str:
    return jwt.encode(
        {
            "id": user.id,
            "is_superuser": user.isSuperuser,
            "is_active": user.isActive,
            "created_at": str(user.createdAt),
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(seconds=settings.refresh_expires),
        },
        settings.refresh_secret_key,
        algorithm="HS256",
    )


async def decode_refresh_token(authorization: str = Header()) -> UserToken | bool:
    try:
        token = jwt.decode(
            authorization,
            settings.refresh_secret_key,
            leeway=datetime.timedelta(seconds=settings.refresh_expires),
            algorithms=["HS256"],
        )
        return UserToken(
            id=token["id"],
            isSuperuser=token["is_superuser"],
            isActive=token["is_active"],
            createdAt=token["created_at"],
        )

    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(401, "INVALID_SIGNATURE")

    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, "TOKEN_HAS_EXPIRED")

    except jwt.exceptions.DecodeError:
        raise HTTPException(401, "TOKEN_INVALID")
