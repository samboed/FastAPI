from typing import List

from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


role_permissions = Table(
    'role_permissions',
    Base.metadata,
Column('role_id',
           ForeignKey('roles.id'),
           primary_key=True),
    Column('permission_id',
           ForeignKey('permissions.id'),
           primary_key=True)

)


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id',
           ForeignKey('users.id'),
           primary_key=True),
    Column('role_id',
           ForeignKey('roles.id'),
           primary_key=True)
)


class Permission(Base):
    __tablename__ = 'permissions'

    write: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    delete: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    only_own: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class Role(Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50),
                                      unique=True, nullable=False)

    permissions: Mapped[List[Permission]] = relationship(secondary=role_permissions,
                                                         lazy="selectin")


class User(Base):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(String(30), unique=True,
                                       index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)

    tokens = relationship('Token', back_populates='user',
                          cascade='all, delete-orphan')
    roles: Mapped[List[Role]] = relationship(secondary=user_roles,
                                             lazy="selectin")
