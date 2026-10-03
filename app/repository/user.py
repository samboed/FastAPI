from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


async def get_user(session: AsyncSession,
                   login: str) -> User | None:
    stm = select(User).where(User.login == login)

    res = await session.execute(stm)

    return res.scalar_one_or_none()
