from fastapi import APIRouter

from app.schemas.user import UserCreate, UserRead, UserUpdate, UserDelete
from app.api.dependencies import DatabaseSessionDep, CurrentUserDep
from app.services.user import (register_user, get_user_by_id,
                               update_user_info_by_id, remove_user)


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('',
             response_model=UserRead)
async def register_new_user(
        user: UserCreate,
        db_session: DatabaseSessionDep
):
    user = await register_user(db_session, user)

    return user


@router.get('/{user_id}',
            response_model=UserRead)
async def get_user(
        user_id: int,
        db_session: DatabaseSessionDep
):
    user = await get_user_by_id(db_session, user_id)

    return user


@router.patch('/{user_id}',
              response_model=UserRead)
async def update_user(
        current_user: CurrentUserDep,
        user: UserUpdate,
        user_id: int,
        db_session: DatabaseSessionDep
):
    user = await update_user_info_by_id(db_session, current_user,
                                        user_id, user)

    return user


@router.delete('/{user_id}',
               response_model=UserDelete)
async def delete_user(
        current_user: CurrentUserDep,
        user_id: int,
        db_session: DatabaseSessionDep
):
    await remove_user(db_session, current_user, user_id)
