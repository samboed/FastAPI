from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    login: str = Field(min_length=1, max_length=256)
    password: str = Field(min_length=1, max_length=256)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str | None = Field("Bearer")
    expires_in: int | None = None
