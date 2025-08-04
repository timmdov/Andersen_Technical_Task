from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str,expires_delta: Optional[timedelta] = None,) -> str:
    now = datetime.utcnow()
    expire = now + (expires_delta if expires_delta is not None else settings.access_token_expire_delta)
    to_encode = {
        "sub": subject,
        "iat": now,
        "exp": expire,
    }
    token = jwt.encode(to_encode, settings.get_secret_key(), algorithm=settings.ALGORITHM)
    return token

def decode_access_token(token: str) -> str:
    payload = jwt.decode(token, settings.get_secret_key(), algorithms=[settings.ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise JWTError("Missing subject")
    return username
