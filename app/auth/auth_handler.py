from datetime import datetime, timedelta
from typing import Optional
import time
import jwt
# from jose import JWTError, jwt
import os

API_SECRET_KEY = "secret"
API_ALGORITHM = "HS256"
API_ACCESS_TOKEN_EXPIRE_MINUTES =  60
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt

def create_refresh_token(email):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={'sub': email}, expires_delta=expires)

def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token

def decodeJWT(token: str) -> dict:
    try:
        decode_token = jwt.decode(token,API_SECRET_KEY, algorithms=[API_ALGORITHM])
        expires = decode_token.get("exp")
        return decode_token if expires >= time.time() else None
    except:
        return {}