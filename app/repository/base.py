import datetime

from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import ModelType


async def add_item(session: AsyncSession,
                   model: type[ModelType],
                   item_data: dict[str, Any]) -> ModelType:
    item = model(**item_data)

    session.add(item)

    try:
        await session.commit()
    except IntegrityError as ex:
        await session.rollback()

        if getattr(ex.orig, "pgcode", None) == '23505':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'{model.__name__.capitalize()} already exists')

        raise

    return item


async def get_item(session: AsyncSession,
                   model: type[ModelType],
                   item_id: int) -> ModelType:
    stm = select(model).where(model.id == item_id)
    res = await session.execute(stm)

    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{model.__name__.capitalize()} with id={item_id} not found')

    return item


async def get_items(session: AsyncSession,
                    model: type[ModelType],
                    conditions: list[BinaryExpression]) -> list[ModelType]:
    stm = select(model).where(*conditions)
    res = await session.execute(stm)

    items = res.scalars().all()

    return items


async def update_item(session: AsyncSession, model: type[ModelType],
                      item_id: int, update_item_data: dict) -> ModelType:
    item = await get_item(session, model, item_id)

    for key, val in update_item_data.items():
        setattr(item, key, val)

    await session.commit()
    await session.refresh(item)

    return item


async def delete_item(session: AsyncSession,
                      model: type[ModelType],
                      item_id: int) -> ModelType:
    item = await get_item(session, model, item_id)

    await session.delete(item)
    await session.commit()


def get_filter_conditions(model: type[ModelType],
                          filter_params: dict) -> list[BinaryExpression]:
    return [
        getattr(model, param) == val
        for param, val in filter_params.items()
    ]


def get_filter_condition_by_created_at(model: type[ModelType],
                                       filter_value: str) -> list[BinaryExpression]:
    if not filter_value:
        return []

    start_time = datetime.datetime.combine(filter_value, datetime.time.min)
    end_time = start_time + datetime.timedelta(days=1)

    return [
        getattr(model, 'created_at') >= start_time,
        getattr(model, 'created_at') < end_time
    ]
