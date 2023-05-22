from fastapi import APIRouter, Depends, Request, status

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
async def register_user(body: UserRegister, request: Request) -> UserOutput:
    return await service.register_user(body, request)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserAuth)
async def login_user(body: UserLogin, request: Request) -> UserAuth:
    return await service.login_user(body, request)


@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=UserAuth)
async def refresh_token(
    request: Request, user: UserToken = Depends(decode_refresh_token)
) -> UserAuth:
    return await service.generate_auth_user(user, request)


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def get_user(
    request: Request, user: UserToken = Depends(decode_token_jwt)
) -> UserOutput:
    return await service.get_user(user, request)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def get_user_by_id(id: int, request: Request) -> UserOutput:
    return await service.get_user_by_id(id, request)


@router.put("/", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def update_user(
    body: UserEdit, request: Request, user: UserToken = Depends(decode_token_jwt)
) -> UserOutput:
    return await service.update_user(user, body, request)


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(request: Request, body: UserForgotPassword) -> None:
    await service.update_password(body, request)
