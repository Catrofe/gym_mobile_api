from typing import Union

import bcrypt
from fastapi import status

from gym_project.api.users.models import UserAuth, UserLogin, UserOutput, UserRegister
from gym_project.api.users.repository import UserRepository
from gym_project.infra.Entities.entities import User
from gym_project.utils.auth_utils import (
    UserToken,
    encode_token_jwt,
    generate_refresh_token,
)
from gym_project.utils.erros_util import RaiseErrorGym


class UserService:
    def __init__(self) -> None:
        self._repository = UserRepository()

    async def register_user(self, user_request: UserRegister) -> UserOutput:
        try:
            if await self._repository.user_is_valid(user_request):
                user_request.password = await self.encode_password(
                    user_request.password
                )
                user = await self._repository.register_user(user_request)
                return UserOutput(**user.dict())

            raise RaiseErrorGym(status.HTTP_400_BAD_REQUEST, "User already exists")
        except Exception as errors:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(errors))

    async def login_user(self, user_request: UserLogin) -> UserAuth:
        try:
            user = await self._repository.login_user(user_request)
            if user:
                if await self.verify_correct_password(
                    user_request.password, user.password
                ):
                    return await self.generate_auth_user(user)
                else:
                    raise RaiseErrorGym(
                        status.HTTP_400_BAD_REQUEST, "Password or login incorrect"
                    )

            raise RaiseErrorGym(status.HTTP_400_BAD_REQUEST, "User not found")
        except Exception as errors:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(errors))

    async def encode_password(self, raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()

    async def verify_correct_password(
        self, raw_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(
            raw_password.encode("utf8"), hashed_password.encode("utf8")
        )

    async def generate_auth_user(self, user: Union[User | UserToken]) -> UserAuth:
        access_token = await encode_token_jwt(user)
        refresh_token = await generate_refresh_token(user)
        return UserAuth(access_token=access_token, refresh_token=refresh_token)

    async def get_user(self, user_request: UserToken) -> UserOutput:
        try:
            user = await self._repository.get_user(user_request.id)
            if user:
                return UserOutput(**user.dict())

            raise RaiseErrorGym(status.HTTP_400_BAD_REQUEST, "User not found")
        except Exception as errors:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(errors))

    async def get_user_by_id(self, user_id: int) -> UserOutput:
        try:
            user = await self._repository.get_user(user_id)
            if user:
                return UserOutput(**user.dict())

            raise RaiseErrorGym(status.HTTP_400_BAD_REQUEST, "User not found")
        except Exception as errors:
            raise RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, str(errors))
