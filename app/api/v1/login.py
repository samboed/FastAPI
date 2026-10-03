from fastapi import APIRouter

from app.schemas.login import UserLogin, TokenResponse
from app.api.dependencies import DatabaseSessionDep
from app.services.login import authenticate_user


router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post('',
             response_model=TokenResponse)
async def login_user(
        credentials: UserLogin,
        db_session: DatabaseSessionDep
):
    token = await authenticate_user(db_session, credentials)

    return token
