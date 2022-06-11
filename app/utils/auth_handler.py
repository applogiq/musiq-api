from datetime import datetime, timedelta
from typing import Optional
import time
import jwt
from decouple import config
from services.user_service import *


API_SECRET_KEY = config("SECRET")
API_ALGORITHM = config("ALGORITHM")
API_ACCESS_TOKEN_EXPIRE_MINUTES =  60
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
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
    return create_token(data={'sub': email}, expires_delta=expires)

def create_access_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token

def decodeJWT(token: str) -> dict:
    try:
        decode_token = jwt.decode(token,API_SECRET_KEY, algorithms=[API_ALGORITHM])
        expires = decode_token.get("exp")
        return decode_token if expires >= time.time() else None
    except:
        return {}


def rolecheck(email):
    user = get_email(email)
    print(user.username)
    return True