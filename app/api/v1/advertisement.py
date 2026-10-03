from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import DatabaseSessionDep
from app.models.advertisement import Advertisement
from app.repository.base import add_item, get_item, get_filter_condition_by_created_at, get_filter_conditions, \
    get_items, update_item, delete_item
from app.schemas.advertisement import AdvertisementCreate, AdvertisementResponse, AdvertisementFilterParams, AdvertisementUpdate


router = APIRouter(
    prefix='/advertisement',
    tags=['Advertisement']
)


@router.post('')
async def add_ad(db_session: DatabaseSessionDep,
                 item_data: AdvertisementCreate) -> AdvertisementResponse:
    item_data_dict = item_data.model_dump(exclude_unset=True)
    item = await add_item(db_session, Advertisement, item_data_dict)
    return AdvertisementResponse(**item.to_dict())


@router.get('/{item_id}')
async def get_ad(db_session: DatabaseSessionDep,
                 item_id: int) -> AdvertisementResponse:
    item = await get_item(db_session, Advertisement, item_id)
    return AdvertisementResponse(**item.to_dict())


@router.get('')
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


@router.patch('/{item_id}')
async def update_ad(db_session: DatabaseSessionDep,
                    item_data: AdvertisementUpdate,
                    item_id: int) -> AdvertisementResponse:
    item_data_dict = item_data.model_dump(exclude_unset=True)
    item = await update_item(db_session, Advertisement, item_id, item_data_dict)
    return AdvertisementResponse(**item.to_dict())


@router.delete('/{item_id}')
async def remove_ad(db_session: DatabaseSessionDep,
                    item_id: int):
    await delete_item(db_session, Advertisement, item_id)
    return {'message': f'{Advertisement.__name__} '
                       f'with id={item_id} '
                       f'was successfully deleted'}
