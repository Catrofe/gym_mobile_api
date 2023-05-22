from fastapi import APIRouter, Depends, status

from gym_project.api.users.models import (
    UserAuth,
    UserEdit,
    UserForgotPassword,
    UserLogin,
    UserOutput,
    UserRegister,
)
from gym_project.api.users.service import UserService
from gym_project.utils.auth_utils import (
    UserToken,
    decode_refresh_token,
    decode_token_jwt,
)

service = UserService()

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOutput)
async def register_user(body: UserRegister) -> UserOutput:
    return await service.register_user(body)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserAuth)
async def login_user(body: UserLogin) -> UserAuth:
    return await service.login_user(body)


@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=UserAuth)
async def refresh_token(user: UserToken = Depends(decode_refresh_token)) -> UserAuth:
    return await service.generate_auth_user(user)


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def get_user(user: UserToken = Depends(decode_token_jwt)) -> UserOutput:
    return await service.get_user(user)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def get_user_by_id(id: int) -> UserOutput:
    return await service.get_user_by_id(id)


@router.put("/", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def update_user(
    body: UserEdit, user: UserToken = Depends(decode_token_jwt)
) -> UserOutput:
    return await service.update_user(user, body)


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(body: UserForgotPassword) -> None:
    await service.update_password(body)
