from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.repository.base import (add_item, get_item,
                                 update_item, delete_item)


async def register_user(db_session: AsyncSession, user: UserCreate):
    user.password = hash_password(user.password)

    user = await add_item(db_session, User, user.model_dump())

    return user


async def get_user_by_id(db_session: AsyncSession, user_id: int):
    user = await get_item(db_session, User, user_id)

    return user

async def update_user_info_by_id(db_session: AsyncSession, user_id: int,
                                 user: UserUpdate):
    update_data = user.model_dump()

    user = await update_item(db_session, User, user_id, update_data)

    return user


async def remove_user(db_session: AsyncSession, user_id: int):
    await delete_item(db_session, User, user_id)
