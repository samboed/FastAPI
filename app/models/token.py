from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .user import User


class Token(Base):
    __tablename__ = 'tokens'

    access_token: Mapped[str] = mapped_column(String, unique=True,
                                       index=True)
    user_id: Mapped['User'] = mapped_column(ForeignKey(User.id,
                                                       ondelete='CASCADE'))

    user = relationship(User, back_populates='tokens')
