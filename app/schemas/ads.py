import datetime

from pydantic import BaseModel


class AdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author: str
    created_at: datetime.datetime


class AdvertisementCreate(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
    author: str | None = None


class AdvertisementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None


class AdvertisementFilterParams(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
    price: float | None = None
    created_at: datetime.datetime | None = None
