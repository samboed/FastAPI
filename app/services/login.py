from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import check_password, create_access_token
from app.schemas.login import UserLogin
from app.repository.user import get_user
from app.repository.base import add_item
from app.models.token import Token


async def authenticate_user(db_session: AsyncSession, credentials: UserLogin):
    user = await get_user(db_session, credentials.login)

    if not user:
        raise HTTPException(403, {
            "error": 'forbidden',
            "message": 'wrong login or password'
        })

    res_checking = check_password(credentials.password, user.password)

    if not res_checking:
        raise HTTPException(403, {
            "error": 'forbidden',
            "message": 'wrong login or password'
        })

    access_token = create_access_token()

    token = await add_item(db_session, Token,
                           item_data={'user_id': user.id,
                                      'access_token': access_token})

    return token



