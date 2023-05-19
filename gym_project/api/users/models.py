from pydantic import BaseModel, Field

_email_field = Field(
    min_length=7,
    max_length=70,
    regex=r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
)


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