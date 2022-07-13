from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
import base64
from fastapi import HTTPException

# from model.song_model import songs
from model.album_model import albums
from services.album_service import *

###response of creating album detail
def create_album_detail(db: Session,album,email):
    if albumname_check(album.album_name,db):
        raise HTTPException(status_code=400, detail="Album is already register")
    try:
        return {"status": True,"message":"data added","records":album_create(db,album,email)}
    except:
        raise HTTPException(status_code=422, detail={"message": "couldn't create,check your details","success":False})

###response of getting all album details
def get_all_album_detail(db,skip,limit):
    try:
        temp = album_get_all(db,skip,limit)
        if len(temp):
            s = len(temp)
        else:
            s = 1
        return {"success":True,"message": "Fetched Successfully","records": temp,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

###response of fetching detail of particular album
def get_album_by_id(album_id,db):
    db_album= album_get_by_id(album_id,db)
    if db_album:
        return {"success":True,"message": "Fetched Successfully","records": db_album,"totalrecords" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

###response of updating existing album detail
def update_album(db,album_id,album,email):
    db_album = album_update(db,album_id,album,email)
    if db_album:
        return {"success": True,"message":"album details updated Successfully","records":db_album}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "album details doesn't exist"})

###response of removing image from particular album detail
def delete_album_image(db,album_id):
    db_album = album_image_delete(db,album_id)
    if db_album:
        return {"success": True,"message":"image removed from album details"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "album details doesn't exist"})
