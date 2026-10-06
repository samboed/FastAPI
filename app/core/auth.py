from sqlalchemy import select, func

from app.database import  AsyncSession
from app.models.user import User, Permission, user_roles, Role, role_permissions


async def check_object_access(
        db_session: AsyncSession,
        user: User,
        resource,
        read: bool = False,
        write: bool = False,
        delete: bool = False) -> bool:
    where_args = [
        User.id == user.id,
    ]
    if read:
        where_args.append(Permission.read == True)

    if write:
        where_args.append(Permission.write == True)

    if delete:
        where_args.append(Permission.delete == True)

    if not isinstance(resource, type):
        if hasattr(resource, 'owner_id'):
            if resource.owner_id != user.id:
                where_args.append(Permission.only_own == False)
        else:
            if resource.id != user.id:
                where_args.append(Permission.only_own == False)

    query = (
        select(func.count())
        .select_from(User)
        .join(user_roles, User.id == user_roles.c.user_id)
        .join(Role, user_roles.c.role_id == Role.id)
        .join(role_permissions, Role.id == role_permissions.c.role_id)
        .join(Permission, role_permissions.c.permission_id == Permission.id)
        .where(*where_args)
    )

    result = await db_session.execute(query)
    count = result.scalar()

    return count > 0
