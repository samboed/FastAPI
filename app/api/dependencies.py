from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.core.exceptions import UnauthorizedError
from app.repository.base import get_item
from app.models.user import User
from app.database import get_db_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/login')


credentials_error = UnauthorizedError(
    message='Invalid authentication credentials'
)

DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


async def get_current_user(db_session: DatabaseSessionDep,
                           access_token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_access_token(access_token)
    if payload is None:
        raise credentials_error

    try:
        user_id = int(payload.get('sub'))
    except (ValueError, TypeError):
        raise credentials_error

    user = await get_item(db_session, User, user_id)
    if not user:
        raise credentials_error

    return user

CurrentUserDep = Annotated[User, Depends(get_current_user)]
