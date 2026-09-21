from sqlalchemy.ext.asyncio import create_async_engine

DSN = ''


AsyncSession = create_async_engine(DSN)
