from fastapi import FastAPI

from app.core.config import DEBUG
from app.core.lifespan import lifespan
from app.api.v1 import api_v1_router


app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisements',
    version='0.0.4',
    lifespan=lifespan
)


app.include_router(api_v1_router)
