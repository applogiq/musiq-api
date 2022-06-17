from datetime import datetime, timedelta
from typing import Optional
import time
import jwt
from decouple import config
from services.user_service import *


ACCESS_SECRET_KEY = config("ACCESS_SECRET")
REFRESH_SECRET_KEY = config("REFRESH_SECRET")
API_ALGORITHM = config("ALGORITHM")
API_ACCESS_TOKEN_EXPIRE_MINUTES =  60 * 24 * 5
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 10

def refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt

def access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt



def create_refresh_token(email):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return refresh_token(data={'sub': email}, expires_delta=expires)

def create_access_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    token = access_token(data={'sub': email}, expires_delta=access_token_expires)
    return token

def decodeJWT(token: str) -> dict:
    # try:
    # s = access_token_check(token)
    # print(1111111)
    decode_token = jwt.decode(token,ACCESS_SECRET_KEY, algorithms=[API_ALGORITHM])
    expires = decode_token.get("exp")
    return decode_token if expires >= time.time() else None
    # except:
    #     return {}


