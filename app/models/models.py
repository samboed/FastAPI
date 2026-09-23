import datetime
from typing import TypeVar

from sqlalchemy.sql.functions import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.types import Text, String, Numeric, Integer, DateTime


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


ModelType = TypeVar("ModelType", bound=Base)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    title: Mapped[str] = mapped_column(Text())
    description: Mapped[str] = mapped_column(String(250))
    price: Mapped[float] = mapped_column(Numeric())
    author_id: Mapped[int] = mapped_column(Integer(), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,
                                                          server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "author_id": self.author_id,
            "created_at": self.created_at
        }
