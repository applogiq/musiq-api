from sqlalchemy.orm import Session
from datetime import datetime
import os
import shutil
import base64
from fastapi import HTTPException

from services.album_service import *

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

