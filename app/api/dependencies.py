from typing import Annotated

from fastapi import Depends
from app.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db_session)]
