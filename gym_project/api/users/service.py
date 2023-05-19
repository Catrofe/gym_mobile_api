from gym_project.api.users.models import UserRegister, UserOutput
from gym_project.api.users.repository import UserRepository
import bcrypt

from fastapi import status
from gym_project.utils.erros_util import RaiseErrorGym


class UserService:

    def __init__(self):
        self._repository = UserRepository()

    async def register_user(self, user_request: UserRegister) -> UserOutput:
        try:
            user_valid = await self._repository.user_is_valid(user_request)
            if await self._repository.user_is_valid(user_request):
                user_request.password = await self.encode_password(user_request.password)
                user = await self._repository.register_user(user_request)
                print(user)
                print(type(user))
                print(user.email)

                return user, None
            return None, status.HTTP_409_CONFLICT
        except Exception as errors:
            return RaiseErrorGym(status.HTTP_500_INTERNAL_SERVER_ERROR, errors)

    async def encode_password(self, raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode("utf8"), bcrypt.gensalt(8)).decode()
