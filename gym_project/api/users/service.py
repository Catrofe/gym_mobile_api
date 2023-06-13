import bcrypt
from fastapi import Request, status

from gym_project.api.auth.models import LoginToken
from gym_project.api.users.models import (
    UserEdit,
    UserForgotPassword,
    UserOutput,
    UserRegister,
)
from gym_project.api.users.repository import UserRepository
from gym_project.utils.erros_util import RaiseErrorGym


class UserService:
    def __init__(self) -> None:
        self._repository = UserRepository()

    async def register_user(
        self, user_request: UserRegister, request: Request
    ) -> UserOutput:
        if not await self._repository.user_is_valid(user_request):
            user_request.password = await self.encode_password(user_request.password)
            user = await self._repository.register_user(user_request)
            return UserOutput(**user.dict())

        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "User already exists")

    async def encode_password(self, raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()

    async def verify_correct_password(
        self, raw_password: str, hashed_password: str
    ) -> bool:
        return bcrypt.checkpw(
            raw_password.encode("utf8"), hashed_password.encode("utf8")
        )

    async def get_user(self, user_request: LoginToken, request: Request) -> UserOutput:
        user = await self._repository.get_user(user_request.id)
        if user:
            return UserOutput(**user.dict())

        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "User not found")

    async def get_user_by_id(self, user_id: int, request: Request) -> UserOutput:
        user = await self._repository.get_user(user_id)
        if user:
            return UserOutput(**user.dict())

        raise RaiseErrorGym(request, status.HTTP_404_NOT_FOUND, "User not found")

    async def update_user(
        self, user_token: LoginToken, user_request: UserEdit, request: Request
    ) -> UserOutput:
        if not await self._repository.user_is_valid_to_edit(user_request):
            if user_request.password:
                user_request.password = await self.encode_password(
                    user_request.password
                )
            user = await self._repository.update_user(user_token.id, user_request)
            if user:
                return UserOutput(**user.dict())

        raise RaiseErrorGym(
            request, status.HTTP_400_BAD_REQUEST, "User not valid to edit"
        )

    async def update_password(
        self, user_request: UserForgotPassword, request: Request
    ) -> bool:
        if await self._repository.verify_if_is_user(user_request):
            if user_request.password == user_request.confirmPassword:
                user_request.password = await self.encode_password(
                    user_request.password
                )
                await self._repository.update_password(user_request)
                return True
            raise RaiseErrorGym(
                request, status.HTTP_400_BAD_REQUEST, "Passwords do not match"
            )
        raise RaiseErrorGym(request, status.HTTP_400_BAD_REQUEST, "User not found")
