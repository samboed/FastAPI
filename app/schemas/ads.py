import datetime

from pydantic import BaseModel


class AdResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    created_at: datetime.datetime


class AdCreate(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None
