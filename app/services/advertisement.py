from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import check_object_access
from app.core.exceptions import ForbiddenError
from app.repository.base import (add_created_item, get_item,
                                 get_filter_condition_by_created_at,
                                 get_filter_conditions,
                                 get_items, update_item, delete_item)
from app.schemas.advertisement import AdvertisementCreate, AdvertisementFilterParams, AdvertisementUpdate
from app.models.advertisement import Advertisement
from app.models.user import User


async def add_advertisement(db_session: AsyncSession, current_user: User,
                            advertisement_data: AdvertisementCreate):
    access = await check_object_access(db_session, current_user, Advertisement, write=True)
    if not access:
        raise ForbiddenError()

    advertisement = Advertisement(owner_id=current_user.id,
                                  **advertisement_data.model_dump(exclude_unset=True))

    new_advertisement = await add_created_item(db_session, advertisement)

    return new_advertisement


async def get_advertisement_by_id(db_session: AsyncSession,
                                  advertisement_id: int) -> Advertisement:
    advertisement = await get_item(db_session, Advertisement, advertisement_id)

    return advertisement


async def get_all_advertisements(db_session: AsyncSession,
                             filter_params: AdvertisementFilterParams) -> list[Advertisement]:
    filter_params_dict = filter_params.model_dump(exclude_unset=True)

    conditions = []
    if 'created_at' in filter_params_dict:
        filter_created_at = filter_params_dict.pop('created_at')
        conditions.extend(get_filter_condition_by_created_at(Advertisement,
                                                             filter_created_at))

    conditions.extend(get_filter_conditions(Advertisement, filter_params_dict))

    advertisements = await get_items(db_session, Advertisement, conditions)

    return advertisements


async def update_advertisement_info(db_session: AsyncSession,
                                    current_user: User,
                                    item_id: int,
                                    advertisement_data:
                                    AdvertisementUpdate) -> Advertisement:
    advertisement_data_dict = advertisement_data.model_dump(exclude_unset=True)

    advertisement = await get_item(db_session,
                                   Advertisement, item_id)

    access = await check_object_access(db_session, current_user,
                                       advertisement, write=True)
    if not access:
        raise ForbiddenError()

    updated_advertisement = await update_item(db_session,
                                              advertisement,
                                              advertisement_data_dict)

    return updated_advertisement


async def remove_advertisement(db_session: AsyncSession, current_user: User,
                               advertisement_id: int):
    advertisement = await get_item(db_session, Advertisement, advertisement_id)

    access = await check_object_access(db_session, current_user,
                                       advertisement, delete=True)
    if not access:
        raise ForbiddenError()

    await delete_item(db_session, advertisement)