from fastapi import APIRouter, Depends, Request, status

from gym_project.api.auth.models import LoginToken
from gym_project.api.users.models import (
    UserEdit,
    UserForgotPassword,
    UserOutput,
    UserRegister,
)
from gym_project.api.users.service import UserService
from gym_project.utils.auth_utils_poc import is_common_user, jwt_authorization

service = UserService()

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOutput)
async def register_user(body: UserRegister, request: Request) -> UserOutput:
    return await service.register_user(body, request)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_common_user)],
    response_model=UserOutput,
)
async def get_user(request: Request) -> UserOutput:
    user = LoginToken(**request.state.user)
    return await service.get_user(user, request)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_common_user)],
    response_model=UserOutput,
)
async def get_user_by_id(id: int, request: Request) -> UserOutput:
    return await service.get_user_by_id(id, request)


@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token), Depends(is_common_user)],
    response_model=UserOutput,
)
async def update_user(body: UserEdit, request: Request) -> UserOutput:
    user = LoginToken(**request.state.user)
    return await service.update_user(user, body, request)


@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(request: Request, body: UserForgotPassword) -> None:
    await service.update_password(body, request)
