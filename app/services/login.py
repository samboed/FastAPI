from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import check_password, create_access_token
from app.core.exceptions import ForbiddenError
from app.schemas.login import UserLogin
from app.repository.user import get_user
from app.repository.base import add_item
from app.models.token import Token


async def authenticate_user(db_session: AsyncSession,
                            credentials: UserLogin):
    user = await get_user(db_session, credentials.login)

    if not user:
        raise ForbiddenError(
            message='Wrong login or password'
        )

    res_checking = check_password(credentials.password, user.password)

    if not res_checking:
        raise ForbiddenError(
            message='Wrong login or password'
        )

    token = await add_item(db_session, Token,
                           item_data={'user_id': user.id})

    payload = {
        'sub': user.id,
        'jti': str(token.jti)
    }

    access_token, expires_in = create_access_token(payload)

    return access_token, expires_in



