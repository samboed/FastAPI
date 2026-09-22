from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.models.models import Base

from app.database.session import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await async_engine.dispose()