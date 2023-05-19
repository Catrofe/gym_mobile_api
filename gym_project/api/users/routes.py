from fastapi import APIRouter, status

from gym_project.api.users.models import UserLogin, UserRegister
from gym_project.api.users.service import UserService
from gym_project.utils.erros_util import RaiseErrorGym

service = UserService()

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(body: UserRegister):
    print("teste")
    response, errors = await service.register_user(body)

    if errors is not None:
        raise RaiseErrorGym(errors)
    return response


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(body: UserLogin):
    response, errors = await service.login_user(body)

    if errors is not None:
        raise RaiseErrorGym(errors)
    return response
