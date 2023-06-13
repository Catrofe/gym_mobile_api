import datetime

import jwt
from fastapi import Request, status

from gym_project.api.auth.models import LoginToken, RoleType
from gym_project.utils.erros_util import RaiseErrorGym
from gym_project.utils.settings import Settings

settings: Settings = Settings()


class AuthManager:
    @staticmethod
    async def encode_token(user: LoginToken, refresh: bool = False) -> str:
        return jwt.encode(
            {
                "id": user.id,
                "is_active": user.is_active,
                "created_at": str(user.created_at),
                "role": user.role,
                "refresh": refresh,
                "exp": (
                    datetime.datetime.now(datetime.timezone.utc)
                    + datetime.timedelta(seconds=settings.secret_expires)
                ),
            },
            settings.refresh_secret_key if refresh else settings.secret_key,
            algorithm="HS256",
        )


class CustomHHTPBearer:
    @staticmethod
    async def decode_token(request: Request) -> None:
        try:
            if authorization := str(request.headers.get("Authorization")):
                authorization = authorization.replace("Bearer ", "")
            refresh = request.url.path == "/api/gym/auth/refresh/"

            token = jwt.decode(
                authorization,
                settings.refresh_secret_key if refresh else settings.secret_key,
                leeway=datetime.timedelta(
                    seconds=settings.refresh_expires
                    if refresh
                    else settings.secret_expires
                ),
                algorithms=["HS256"],
            )
            request.state.user = token
        except Exception as e:
            raise RaiseErrorGym(
                request, status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED"
            ) from e


jwt_authorization = CustomHHTPBearer


async def is_common_user(request: Request) -> None:
    if (
        request.state.user["role"] != RoleType.user.value
        or not request.state.user["is_active"]
    ):
        raise RaiseErrorGym(request, status.HTTP_403_FORBIDDEN, "FORBIDDEN")


async def is_employee(request: Request) -> None:
    if (
        request.state.user["role"]
        not in [RoleType.employee.value, RoleType.admin.value]
        or not request.state.user["is_active"]
    ):
        raise RaiseErrorGym(request, status.HTTP_403_FORBIDDEN, "FORBIDDEN")


async def is_admin(request: Request) -> None:
    if (
        request.state.user["role"] != RoleType.admin.value
        or not request.state.user["is_active"]
    ):
        raise RaiseErrorGym(request, status.HTTP_403_FORBIDDEN, "FORBIDDEN")
