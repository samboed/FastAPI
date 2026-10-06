import datetime

from pydantic import BaseModel


class AdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    owner_id: int
    created_at: datetime.datetime


class AdvertisementCreate(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None


class AdvertisementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class AdvertisementFilterParams(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    created_at: datetime.datetime | None = None


class AdvertisementDelete(BaseModel):
    success: bool | None = True
    message: str | None = 'Advertisement was deleted'
