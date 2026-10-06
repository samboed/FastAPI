from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, Role
from app.repository.base import add_created_item


async def add_user(session: AsyncSession, user_data: dict[str, Any]) -> User | None:
    stm = select(Role).where(Role.name == 'user')

    res = await session.execute(stm)

    user_role = res.scalars().first()

    new_user = User(**user_data, roles=[user_role])

    user = await add_created_item(session, new_user)

    return user


async def get_user(session: AsyncSession,
                   login: str) -> User | None:
    stm = select(User).where(User.login == login)

    res = await session.execute(stm)

    return res.scalar_one_or_none()
