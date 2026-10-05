from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import check_object_access
from app.core.exceptions import ForbiddenError
from app.repository.base import (add_item, get_item,
                                 get_filter_condition_by_created_at,
                                 get_filter_conditions,
                                 get_items, update_item, delete_item)
from app.schemas.advertisement import AdvertisementFilterParams, AdvertisementUpdate
from app.models.advertisement import Advertisement
from app.models.user import User


async def add_advertisement(db_session: AsyncSession, current_user: User, item_data):
    item_data_dict = item_data.model_dump(exclude_unset=True)

    access = await check_object_access(db_session, current_user, Advertisement, write=True)
    if not access:
        raise ForbiddenError()

    item = await add_item(db_session, Advertisement, item_data_dict)

    return item


async def get_advertisement(db_session: AsyncSession, item_id: int):
    item = get_item(db_session, Advertisement, item_id)

    return item


async def get_advertisements(db_session: AsyncSession,
                             filter_params: AdvertisementFilterParams):
    filter_params_dict = filter_params.model_dump(exclude_unset=True)

    conditions = []
    if 'created_at' in filter_params_dict:
        filter_created_at = filter_params_dict.pop('created_at')
        conditions.extend(get_filter_condition_by_created_at(Advertisement,
                                                             filter_created_at))

    conditions.extend(get_filter_conditions(Advertisement, filter_params_dict))

    items = await get_items(db_session, Advertisement, conditions)

    return items


async def update_advertisement_info(db_session: AsyncSession,
                                    current_user: User,
                                    item_id: int,
                                    advertisement_update: AdvertisementUpdate):
    item_data_dict = advertisement_update.model_dump(exclude_unset=True)

    item = await get_item(db_session, Advertisement, item_id)

    access = await check_object_access(db_session, current_user, item, write=True)
    if not access:
        raise ForbiddenError()

    item = await update_item(db_session, item, item_data_dict)

    return item


async def remove_advertisement(db_session: AsyncSession, current_user: User, item_id: int):
    item = await get_item(db_session, Advertisement, item_id)

    access = await check_object_access(db_session, current_user, item, delete=True)
    if not access:
        raise ForbiddenError()

    await delete_item(db_session, item)