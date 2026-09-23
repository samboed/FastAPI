from typing import Any

from pydantic import BaseModel as PydanticModel
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import ModelType


async def add_item(session: AsyncSession,
                   model: ModelType,
                   item_data: PydanticModel) -> ModelType:
    item = model(**item_data.model_dump())

    session.add(item)
    try:
        await session.commit()
        await session.refresh(item)
    except IntegrityError as ex:
        await session.rollback()

        if getattr(ex.orig, "pgcode", None) == '23505':
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'{model.__name__.capitalize()} already exists')

        raise

    return item


async def get_item(session: AsyncSession,
                   model: type[ModelType],
                   item_id: int) -> list[dict[str, Any]]:
    stm = select(model).where(model.id == item_id)
    res = await session.execute(stm)

    item = res.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{model.__name__.capitalize()} with id={item_id} not found')

    return item

async def get_items(session: AsyncSession,
                    model: type[ModelType]) -> list[ModelType]:
    stm = select(model)
    res = await session.execute(stm)

    items = res.scalars().all()

    return items


async def update_item(session: AsyncSession,
                      model: ModelType,
                      update_item_data: PydanticModel,
                      item_id: int) -> ModelType:
    item = await get_item(session, model, item_id)

    update_item_data = update_item_data.model_dump(exclude_unset=True)

    for key, val in update_item_data.items():
        setattr(item, key, val)

    await session.commit()
    await session.refresh(item)

    return item


async def delete_item(session: AsyncSession,
                      model: ModelType,
                      item_id: int) -> ModelType:
    item = await get_item(session, model, item_id)

    await session.delete(item)
    await session.commit()
