from fastapi import FastAPI

from app.core.config import DEBUG
from app.core.dependencies import DatabaseSessionDep
from app.core.lifespan import lifespan
from app.schemas.ads import AdvertisementCreate, AdvertisementUpdate, AdvertisementResponse
from app.models.models import Advertisement
from app.database.repository import (add_item, get_item, get_items,
                                     update_item, delete_item)


app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisement',
    version='0.0.1',
    lifespan=lifespan
)


@app.post('/advertisements')
async def create_ad(db_session: DatabaseSessionDep,
                    item_data: AdvertisementCreate) -> AdvertisementResponse:
    item = await add_item(db_session, Advertisement, item_data)
    return AdvertisementResponse(**item.to_dict())


@app.get('/advertisements/{item_id}')
async def get_ad(db_session: DatabaseSessionDep,
                 item_id: int) -> AdvertisementResponse:
    item = await get_item(db_session, Advertisement, item_id)
    return AdvertisementResponse(**item.to_dict())


@app.get('/advertisements')
async def get_ads(db_session: DatabaseSessionDep) -> list[AdvertisementResponse]:
    items = await get_items(db_session, Advertisement)
    return [AdvertisementResponse(**item.to_dict()) for item in items]


@app.patch('/advertisements/{item_id}')
async def update_ad(db_session: DatabaseSessionDep,
                    item_data: AdvertisementUpdate,
                    item_id: int) -> AdvertisementResponse:
    item = await update_item(db_session, Advertisement, item_data, item_id)
    return AdvertisementResponse(**item.to_dict())


@app.delete('/advertisements/{item_id}')
async def delete_ad(db_session: DatabaseSessionDep,
                    item_id: int):
    await delete_item(db_session, Advertisement, item_id)
    return
