from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import DB_DSN


async_engine = create_async_engine(DB_DSN)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session():
    async with async_session_maker() as session:
        yield session
