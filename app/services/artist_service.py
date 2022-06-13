from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64

from sqlalchemy import null
# from utils.auth_handler import create_access_token
from model.user_model import *
from config.database import *
from model.artist_model import *

def artist_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(artist).filter(artist.is_delete == 0).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

# def artist_image_check(db,id):
#     return db.query(artist).filter(artist.id == id,artist.is_delete == 0,artist.is_image == 1).first()

def artist_get_by_id(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete==0).first()

