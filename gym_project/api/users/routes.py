from fastapi import APIRouter, Depends, status

from gym_project.api.users.models import UserAuth, UserLogin, UserOutput, UserRegister
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
    response = await service.register_user(body)
    return response


@router.post("/login", status_code=status.HTTP_200_OK, response_model=UserAuth)
async def login_user(body: UserLogin) -> UserAuth:
    response = await service.login_user(body)
    return response


@router.get("/refresh", status_code=status.HTTP_200_OK, response_model=UserAuth)
async def refresh_token(user: UserToken = Depends(decode_refresh_token)) -> UserAuth:
    response = await service.generate_auth_user(user)
    return response


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def get_user(user: UserToken = Depends(decode_token_jwt)) -> UserOutput:
    response = await service.get_user(user)
    return response


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserOutput)
async def get_user_by_id(id: int) -> UserOutput:
    response = await service.get_user_by_id(int(id))
    return response
