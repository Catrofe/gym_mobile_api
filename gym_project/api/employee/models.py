from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from gym_project.utils.settings import Settings

_email_field = Field(
    min_length=7,
    max_length=70,
    regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
)

settings: Settings = Settings()


class EmployeeRegister(BaseModel):
    fullName: str = Field(max_length=150)
    username: str = Field(max_length=50)
    cpf: str = Field(max_length=11)
    email: str = _email_field
    phoneNumber: str = Field(max_length=15)
    password: str = Field(max_length=255)


class EmployeeOutput(BaseModel):
    id: int
    fullName: str
    username: str
    cpf: str
    email: str
    phoneNumber: str
    isActive: bool
    isSuperuser: bool
    createdAt: datetime
    updatedAt: datetime | None


class EmployeeLogin(BaseModel):
    login: str
    password: str


class EmployeeAuth(BaseModel):
    access_token: str
    expires_in: int = settings.secret_expires
    refresh_expires_in: int = settings.refresh_expires
    refresh_token: str
    token_type: str = "Bearer"


class EmployeeEdit(BaseModel):
    fullName: Optional[str] = Field(max_length=150)
    email: Optional[str] = _email_field
    phoneNumber: Optional[str] = Field(max_length=15)
    password: Optional[str] = Field(max_length=255)


class EmployeeForgotPassword(BaseModel):
    password: str = Field(max_length=255)
    confirmPassword: str = Field(max_length=255)
    username: str = Field(max_length=50)
    email: str = _email_field
    cpf: str = Field(max_length=11)
    phoneNumber: str = Field(max_length=15)
