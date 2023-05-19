from pydantic import BaseModel, Field

from gym_project.utils.settings import Settings

_email_field = Field(
    min_length=7,
    max_length=70,
    regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
)

settings: Settings = Settings()


class UserRegister(BaseModel):
    fullName: str = Field(max_length=150)
    username: str = Field(max_length=50)
    cpf: str = Field(max_length=11)
    email: str = _email_field
    phoneNumber: str = Field(max_length=15)
    password: str = Field(max_length=255)


class UserOutput(BaseModel):
    id: int
    fullName: str
    username: str
    cpf: str
    email: str
    phoneNumber: str
    isActive: bool
    isSuperuser: bool
    createdAt: str
    updatedAt: str


class UserLogin(BaseModel):
    login: str
    password: str


class UserAuth(BaseModel):
    access_token: str
    expires_in: int = settings.secret_expires
    refresh_expires_in: int = settings.refresh_expires
    refresh_token: str
    token_type: str = "Bearer"
