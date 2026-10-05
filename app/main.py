from fastapi import FastAPI

from app.core.config import DEBUG
from app.core.exception_handlers import app_exception_handler
from app.core.exceptions import AppException
from app.core.lifespan import lifespan
from app.api.v1 import api_v1_router


app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisements',
    version='0.1.5',
    lifespan=lifespan
)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(api_v1_router)
