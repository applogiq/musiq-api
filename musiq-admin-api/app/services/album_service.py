from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64

# from utils.auth_handler import create_access_token
from model.album_model import *
from config.database import *
from model.artist_model import *

def album_get_by_id(id,db):
    return db.query(albums).filter(albums.id == id,albums.is_delete==False).first()

def album_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(albums).filter(albums.is_delete == False).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

    
    

    

    
   