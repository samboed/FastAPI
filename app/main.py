from typing import Annotated
from fastapi import FastAPI, Query, Response

from app.core.config import DEBUG
from app.core.dependencies import DatabaseSessionDep
from app.core.lifespan import lifespan
from app.schemas.ads import (AdvertisementCreate, AdvertisementUpdate,
                             AdvertisementResponse, AdvertisementFilterParams)
from app.models.models import Advertisement
from app.repository.base import (add_item, get_item, get_items,
                                 update_item, delete_item,
                                 get_filter_conditions,
                                 get_filter_condition_by_created_at)

app = FastAPI(
    debug=DEBUG,
    title='API',
    summary='API for advertisements',
    version='0.0.3',
    lifespan=lifespan
)


@app.post('/advertisement')
async def create_ad(db_session: DatabaseSessionDep,
                    item_data: AdvertisementCreate) -> AdvertisementResponse:
    item = await add_item(db_session, Advertisement, item_data)
    return AdvertisementResponse(**item.to_dict())


@app.get('/advertisement/{item_id}')
async def get_ad(db_session: DatabaseSessionDep,
                 item_id: int) -> AdvertisementResponse:
    item = await get_item(db_session, Advertisement, item_id)
    return AdvertisementResponse(**item.to_dict())


@app.get('/advertisement')
async def get_ads(db_session: DatabaseSessionDep,
                  filter_params: Annotated[AdvertisementFilterParams, Query()]) -> list[AdvertisementResponse]:
    filter_params_dict = filter_params.model_dump(exclude_unset=True)
    conditions = []

    if 'created_at' in filter_params_dict:
        filter_created_at = filter_params_dict.pop('created_at')
        conditions.extend(get_filter_condition_by_created_at(Advertisement,
                                                             filter_created_at))

    conditions.extend(get_filter_conditions(Advertisement, filter_params_dict))

    items = await get_items(db_session, Advertisement, conditions)

    return [AdvertisementResponse(**item.to_dict()) for item in items]


@app.patch('/advertisement/{item_id}')
async def update_ad(db_session: DatabaseSessionDep,
                    item_data: AdvertisementUpdate,
                    item_id: int) -> AdvertisementResponse:
    item = await update_item(db_session, Advertisement, item_data, item_id)
    return AdvertisementResponse(**item.to_dict())


@app.delete('/advertisement/{item_id}')
async def delete_ad(db_session: DatabaseSessionDep,
                    item_id: int):
    await delete_item(db_session, Advertisement, item_id)
    return {'message': f'{Advertisement.__name__} '
                       f'with id={item_id} '
                       f'was successfully deleted'}
