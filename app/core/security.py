from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

SECRET_KEY = "123456"  # TODO: Get this from config
ALGORITHM = "HS256"

password_hash = PasswordHash.recommended()


def create_password_hash(password: str):
    return password_hash.hash(password)


def verify_password_hash(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None):
    payload = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload.update({"exp": expire})
    jwt_encoded = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return jwt_encoded
