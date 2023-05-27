from enum import Enum

from pydantic import BaseModel

from gym_project.utils.settings import Settings

settings: Settings = Settings()


class RoleType(Enum):
    user = "user"
    employee = "employee"
    admin = "admin"


class LoginAuth(BaseModel):
    login: str
    password: str
    typeUser: RoleType = RoleType.user


class LoginAuthResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer "
    expires_in: int = settings.secret_expires
    refresh_token: str
    refresh_expires_in: int = settings.refresh_expires


class LoginToken(BaseModel):
    id: int
    is_active: bool
    created_at: str
    role: str
    refresh: bool = False
