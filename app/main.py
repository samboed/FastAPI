from fastapi import FastAPI
from sqlalchemy import select

from app.core.config import DEBUG
from app.core.dependencies import DatabaseSessionDep
from app.core.lifespan import lifespan
from app.schemas.ads import AdCreate, AdResponse
from app.models.models import Advertisement


app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisement',
    version='0.0.1',
    lifespan=lifespan
)


@app.get('/advertisements')
async def get_ads(db_session: DatabaseSessionDep) -> list[AdResponse]:
    stm = select(Advertisement)
    res = await db_session.execute(stm)
    return [AdResponse(**item.to_dict()) for item in res.scalars().all()]


@app.post('/advertisements')
async def create_ad(ad: AdCreate, db_session: DatabaseSessionDep) -> AdResponse:
    item = Advertisement(**ad.model_dump())
    db_session.add(item)
    await db_session.commit()
    return AdResponse(**item.to_dict())
