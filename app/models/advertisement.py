import datetime

from sqlalchemy.sql.functions import func
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.types import Text, String, Integer, Numeric, DateTime

from app.models.base import Base


class Advertisement(Base):
    __tablename__ = 'advertisements'

    title: Mapped[str] = mapped_column(Text())
    description: Mapped[str] = mapped_column(String(250))
    owner_id: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Numeric(), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime,
                                                          server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "owner_id": self.owner_id,
            "created_at": self.created_at
        }
