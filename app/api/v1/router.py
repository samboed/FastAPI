from fastapi import APIRouter

from .login import router as login_router
from .user import router as user_router
from .advertisement import router as advertisement_router


api_v1_router = APIRouter(
    prefix='/api/v1'
)

api_v1_router.include_router(login_router)
api_v1_router.include_router(user_router)
api_v1_router.include_router(advertisement_router)
