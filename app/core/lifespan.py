from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.user import Permission, Role

from app.database import async_engine, async_session_maker


async def seed_data(session):
    own_read_write_delete_permissions = Permission(
        read=True, write=True, delete=True, only_own=True
    )
    only_read_permissions = Permission(
        read=True, write=False, delete=False, only_own=False
    )
    full_permissions = Permission(
        read=True, write=True, delete=True, only_own=False
    )

    role_user = Role(name="user")
    role_user.permissions = [only_read_permissions, own_read_write_delete_permissions]

    role_admin = Role(name="admin")
    role_admin.permissions = [full_permissions]

    session.add_all([own_read_write_delete_permissions, only_read_permissions, full_permissions])
    session.add_all([role_user, role_admin])

    try:
        await session.commit()
    except IntegrityError:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        await seed_data(session)

    yield

    await async_engine.dispose()
