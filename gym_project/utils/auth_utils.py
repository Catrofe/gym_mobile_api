import datetime
from typing import Union

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
            isSuperuser=token["is_superuser"],
            isActive=token["is_active"],
            createdAt=token["created_at"],
        )

    except Exception as e:
        raise HTTPException(401, "UNAUTHORIZED") from e


async def encode_token_jwt(user: Union[User | UserToken]) -> str:
    return jwt.encode(
        {
            "id": user.id,
            "is_superuser": user.isSuperuser,
            "is_active": user.isActive,
            "created_at": str(user.createdAt),
            "exp": (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(seconds=settings.secret_expires)
            ),
        },
        settings.secret_key,
        algorithm="HS256",
    )


async def generate_refresh_token(user: Union[User | UserToken]) -> str:
    return jwt.encode(
        {
            "id": user.id,
            "is_superuser": user.isSuperuser,
            "is_active": user.isActive,
            "created_at": str(user.createdAt),
            "exp": (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(seconds=settings.refresh_expires)
            ),
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

    except jwt.exceptions.InvalidSignatureError as e:
        raise HTTPException(401, "INVALID_SIGNATURE") from e

    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(401, "TOKEN_HAS_EXPIRED") from e

    except jwt.exceptions.DecodeError as e:
        raise HTTPException(401, "TOKEN_INVALID") from e
