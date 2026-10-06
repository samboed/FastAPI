from pydantic import BaseModel, Field, ConfigDict


class UserCreate(BaseModel):
    login: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=64)
    first_name: str = Field(min_length=3, max_length=30)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None = None
    last_name: str | None = None


class UserUpdate(BaseModel):
    first_name: str
    last_name: str


class UserDelete(BaseModel):
    success: bool | None = True
    message: str | None = 'User was deleted'
