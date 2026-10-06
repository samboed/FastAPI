from typing import Annotated

from fastapi import APIRouter, Query

from app.api.dependencies import CurrentUserDep, DatabaseSessionDep
from app.services.advertisement import (add_advertisement, get_advertisement_by_id,
                                        get_all_advertisements, update_advertisement_info,
                                        remove_advertisement)
from app.models.advertisement import Advertisement
from app.schemas.advertisement import (AdvertisementCreate, AdvertisementResponse,
                                       AdvertisementFilterParams, AdvertisementUpdate,
                                       AdvertisementDelete)


router = APIRouter(
    prefix='/advertisement',
    tags=['Advertisement']
)


@router.post('',
             response_model=AdvertisementResponse)
async def create_advertisement(current_user: CurrentUserDep,
                               db_session: DatabaseSessionDep,
                               item_data: AdvertisementCreate):
    item = await add_advertisement(db_session, current_user, item_data)
    return item.to_dict()


@router.get('/{item_id}',
            response_model=AdvertisementResponse)
async def get_advertisement(db_session: DatabaseSessionDep,
                            item_id: int):
    item = await get_advertisement_by_id(db_session, item_id)
    return item.to_dict()


@router.get('',
            response_model=list[AdvertisementResponse])
async def get_advertisements(db_session: DatabaseSessionDep,
                             filter_params: Annotated[AdvertisementFilterParams, Query()]):
    items = await get_all_advertisements(db_session, filter_params)

    return [AdvertisementResponse(**item.to_dict()) for item in items]


@router.patch('/{item_id}',
              response_model=AdvertisementResponse)
async def update_advertisement(current_user: CurrentUserDep,
                               db_session: DatabaseSessionDep,
                               update_data: AdvertisementUpdate,
                               item_id: int):
    item = await update_advertisement_info(db_session, current_user, item_id, update_data)

    return item.to_dict()


@router.delete('/{item_id}',
               response_model=AdvertisementDelete)
async def delete_advertisement(current_user: CurrentUserDep,
                               db_session: DatabaseSessionDep,
                               item_id: int):
    await remove_advertisement(db_session, current_user, item_id)

    return AdvertisementDelete(
        message=f'{Advertisement.__name__} '
                f'with id={item_id} '
                f'was successfully deleted'
    )
