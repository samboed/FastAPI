from typing import Annotated

from fastapi import Depends
from app.database.session import async_session_maker
from sqlalchemy.ext.asyncio import AsyncConnection


async def get_db_session():
    async with async_session_maker() as session:
        yield session


DatabaseSessionDep = Annotated[AsyncConnection, Depends(get_db_session)]
