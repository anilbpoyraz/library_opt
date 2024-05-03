from datetime import datetime, timedelta
from typing import Any, Union

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext
from core.config import settings

import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
        subject: Union[dict, Any],expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire}
    to_encode.update(subject)
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, 
        algorithm=settings.HASH_ALGORITHM)

    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print('plain_password: ', plain_password)
    print('hashed_password: ', hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)