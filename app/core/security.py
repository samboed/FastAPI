import bcrypt
import jwt

from typing import Any
from datetime import datetime, timedelta

from app.core.config import JWT_SECRET_KEY, JWT_TTL


ENCODING = 'utf-8'

JWT_ALGORITHM = 'HS256'


def hash_password(password: str) -> str:
    password_bin = password.encode(ENCODING)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bin,
                                    salt)

    return hashed_password.decode(ENCODING)


def check_password(password: str,
                   hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(ENCODING),
                          hashed_password.encode(ENCODING))


def create_access_token(data: dict = None) -> tuple[str, int]:
    if data:
        payload = data.copy()
    else:
        payload = {}

    expire_time = datetime.now() + timedelta(seconds=JWT_TTL)

    payload['exp'] = str(int(expire_time.timestamp()))

    token = jwt.encode(payload, JWT_SECRET_KEY, JWT_ALGORITHM)

    return token, JWT_TTL


def decode_access_token(access_token: str) -> dict[str, Any] | None:
    try:
        payload = jwt.decode(
            access_token,
            JWT_SECRET_KEY,
            [JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None

    return payload
