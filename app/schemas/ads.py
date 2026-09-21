from pydantic import BaseModel


class AdCreate(BaseModel):
    title: str
    description: str | None = None
    price: float | None = None