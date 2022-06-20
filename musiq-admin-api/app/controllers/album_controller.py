from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
import base64
from fastapi import HTTPException

# from model.song_model import songs
from model.album_model import albums
from services.album_service import *

def album_detail(db: Session,album,email):
    if albumname_check(album.name,db):
        raise HTTPException(status_code=400, detail="Album is already register")
    # if album_create(db,album):
        # return {"message":"data added"}
    # try:
    return {"status": True,"message":"data added","records":album_create(db,album,email)}
    # except:
    #     raise HTTPException(status_code=422, detail={"message": "couldn't create,check your details","success":False})

