import uuid

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base
from .user import User


class Token(Base):
    __tablename__ = 'tokens'

    jti: Mapped[uuid.UUID] = mapped_column(UUID,
                                           server_default=func.gen_random_uuid(),
                                           unique=True,
                                           index=True,
                                           nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id,
                                                    ondelete='CASCADE'))

    user: Mapped[User] = relationship(User, back_populates='tokens')
