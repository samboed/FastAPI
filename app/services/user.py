from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.core.exceptions import ForbiddenError
from app.core.auth import check_object_access
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.repository.base import (add_item, get_item,
                                 update_item, delete_item)


async def register_user(db_session: AsyncSession, user: UserCreate):
    user.password = hash_password(user.password)

    user = await add_item(db_session, User, user.model_dump())

    return user


async def get_all_users(db_session: AsyncSession) -> list[User]:
    users = await get_items(db_session, User)

    return users


async def get_user_by_id(db_session: AsyncSession, user_id: int) -> User:
    user = await get_item(db_session, User, user_id)

    return user


async def update_user_info_by_id(db_session: AsyncSession,
                                 current_user: User,
                                 update_user_id: int,
                                 user: UserUpdate):
    update_data = user.model_dump()

    user = await get_item(db_session, User, update_user_id)

    access = await check_object_access(db_session, current_user, user, write=True)
    if not access:
        raise ForbiddenError()

    user = await update_item(db_session, User, update_user_id, update_data)

    return user


async def remove_user(db_session: AsyncSession,
                      current_user: User,
                      user_id: int):
    user = await get_item(db_session, User, user_id)

    access = await check_object_access(db_session, current_user, user, delete=True)
    if not access:
        raise ForbiddenError()

    await delete_item(db_session, user)
