from typing import List

from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


role_permissions = Table(
    'permission_role_relation',
    Base.metadata,
    Column('permission_id',
           ForeignKey('permissions.id'),
           primary_key=True),
    Column('role_id',
           ForeignKey('roles.id'),
           primary_key=True)
)


user_roles = Table(
    'user_role_relation',
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

    roles = relationship('Role',
                         secondary=role_permissions,
                         back_populates='permissions')


class Role(Base):
    __tablename__ = 'roles'

    name: Mapped[str] = mapped_column(String(50),
                                      unique=True, nullable=False)
    permissions: Mapped[List[Permission]] = relationship(Permission,
                                                         secondary=role_permissions,
                                                         back_populates='roles',
                                                         lazy="selectin")

    users = relationship('User',
                         secondary=user_roles,
                         back_populates='roles')


class User(Base):
    __tablename__ = 'users'

    login: Mapped[str] = mapped_column(String(30), unique=True,
                                       index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True)

    tokens = relationship('Token', back_populates='user')
    roles = relationship(Role, secondary=user_roles, back_populates='users',
                         lazy="selectin")
