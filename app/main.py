from typing import Annotated
from fastapi import FastAPI, Query

from app.core.config import DEBUG
from app.core.dependencies import DatabaseSessionDep
from app.core.lifespan import lifespan
from app.schemas.ads import (AdvertisementCreate, AdvertisementUpdate,
                             AdvertisementResponse, AdvertisementFilterParams)
from app.models.models import Advertisement
from app.database.repository import (add_item, get_item, get_items,
                                     update_item, delete_item, 
                                     get_filter_conditions)

app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisements',
    version='0.0.2',
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
async def get_ads(db_session: DatabaseSessionDep,
                  filter_params: Annotated[AdvertisementFilterParams, Query()]) -> list[AdvertisementResponse]:
    conditions = get_filter_conditions(Advertisement, filter_params)
    items = await get_items(db_session, Advertisement, conditions)
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
