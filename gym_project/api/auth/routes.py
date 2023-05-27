from fastapi import APIRouter, Depends, Request, status

from gym_project.api.auth.models import LoginAuth, LoginAuthResponse, LoginToken
from gym_project.api.auth.service import AuthService
from gym_project.utils.auth_utils_poc import jwt_authorization

service = AuthService()
router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK, response_model=LoginAuthResponse)
async def login_employee(body: LoginAuth, request: Request) -> LoginAuthResponse:
    return await service.login(body, request)


@router.get(
    "/refresh/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(jwt_authorization.decode_token)],
    response_model=LoginAuthResponse,
)
async def refresh_token(
    request: Request,
) -> LoginAuthResponse:
    user = request.state.user
    return await service.refresh_token(LoginToken(**user), request)
