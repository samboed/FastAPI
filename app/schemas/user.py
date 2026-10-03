from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=64)
    first_name: str = Field(min_length=3, max_length=30)


class UserRead(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None


class UserUpdate(BaseModel):
    first_name: str
    last_name: str


class UserDelete(BaseModel):
    success: bool = True
    message: str = 'User was deleted'
