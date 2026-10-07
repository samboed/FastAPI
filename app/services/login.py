from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import check_password, create_access_token
from app.core.exceptions import UnauthorizedError
from app.schemas.login import  UserLogin
from app.repository.user import get_user
from app.repository.base import add_item
from app.models.token import Token


FailAuthenticateError = UnauthorizedError(
    message='Wrong login or password'
)


async def authenticate_user(db_session: AsyncSession,
                            credentials: UserLogin):
    user = await get_user(db_session, credentials.username)
    if not user:
        raise FailAuthenticateError

    res_checking = check_password(credentials.password, user.password)
    if not res_checking:
        raise FailAuthenticateError

    token = await add_item(db_session, Token,
                           item_data={'user_id': user.id})

    payload = {
        'sub': str(user.id),
        'jti': str(token.jti)
    }

    access_token, expires_in = create_access_token(payload)

    return access_token, expires_in



