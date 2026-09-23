import datetime

from pydantic import BaseModel


class AdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    author_id: int
    created_at: datetime.datetime


class AdvertisementCreate(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
    author_id: int | None = None


class AdvertisementUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
