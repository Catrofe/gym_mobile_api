from typing import Union

import bcrypt
from fastapi import Request, status

from gym_project.api.auth.models import (
    LoginAuth,
    LoginAuthResponse,
    LoginToken,
    RoleType,
)
from gym_project.api.auth.repository import AuthRepository
from gym_project.infra.Entities.entities import PydanticEmployee, PydanticUser
from gym_project.utils.auth_utils_poc import AuthManager
from gym_project.utils.erros_util import RaiseErrorGym


class AuthService:
    def __init__(self) -> None:
        self._repository = AuthRepository()

    async def login(self, body: LoginAuth, request: Request) -> LoginAuthResponse:
        if body.typeUser.value == RoleType.employee.value:
            user = await self._repository.login_employee_auth(body)
        else:
            user = await self._repository.login_user_auth(body)

        if user:
            if await self.verify_correct_password(body.password, user.password):
                try:
                    token = await self.mapper_login_token(user)
                    return await self.generate_auth(token)
                except Exception as e:
                    raise RaiseErrorGym(
                        request, status.HTTP_500_INTERNAL_SERVER_ERROR, str(e)
                    ) from e
            else:
                raise RaiseErrorGym(
                    request, status.HTTP_400_BAD_REQUEST, "Password or login incorrect"
                )

        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "User not found")

    @staticmethod
    async def verify_correct_password(raw_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode("utf8"), hashed_password.encode("utf8")
        )

    @staticmethod
    async def generate_auth(user: LoginToken) -> LoginAuthResponse:
        access_token = await AuthManager.encode_token(user)
        refresh_token = await AuthManager.encode_token(user, refresh=True)
        return LoginAuthResponse(access_token=access_token, refresh_token=refresh_token)

    async def refresh_token(
        self, body: LoginToken, request: Request
    ) -> LoginAuthResponse:
        if body.role == RoleType.employee.value:
            user = await self._repository.get_employee_by_id(body.id)
        else:
            user = await self._repository.get_user_by_id(body.id)

        if user:
            token = await self.mapper_login_token(user)
            return await self.generate_auth(token)

        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "User not found")

    @staticmethod
    async def mapper_login_token(
        user: Union[PydanticEmployee | PydanticUser],
    ) -> LoginToken:
        role = RoleType.user.value
        if isinstance(user, PydanticEmployee):
            role = RoleType.admin.value if user.isSuperuser else RoleType.employee.value
        return LoginToken(
            id=user.id,
            is_active=user.isActive,
            created_at=str(user.createdAt),
            role=role,
        )
