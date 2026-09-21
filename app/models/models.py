import datetime

from sqlalchemy.sql.functions import func
from sqlalchemy.orm import DeclarativeBase, mapped_column, MappedColumn
from sqlalchemy.types import Text, String, Numeric, Integer, DateTime


class Base(DeclarativeBase):
    id: MappedColumn[int] = mapped_column(primary_key=True)


class Advertisement(Base):
    __tablename__ = 'advertisements'

    title: MappedColumn[str] = mapped_column(Text)
    description: MappedColumn[str] = mapped_column(String(250))
    price: MappedColumn[float] = mapped_column(Numeric)
    author_id: MappedColumn[int] = mapped_column(Integer)
    created_at: MappedColumn[datetime.datetime] = mapped_column(DateTime,
                                                                server_default=func.now)
