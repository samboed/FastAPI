from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel, Field


CredentialsFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str | None = Field("Bearer")
    expires_in: int | None = None
