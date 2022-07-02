from fastapi import HTTPException
import re

from services.artist_service import *

def get_all_artist_detail(db,skip,limit):
    db_artist = artist_get_all(db,skip,limit)
    if db_artist:
        return {"success":True,"message":"details fetched succesfully","records": db_artist,"total_records" : len(db_artist)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_artist_detail_by_id(db,artist_id):
    db_artist = artist_get_by_id(db,artist_id)
    if db_artist:
        return {"success":True,"message":"details fetched succesfully","records": db_artist,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_homepage_artist_detail(db,email):
    db_artist = artist_home_page(db,email)
    if db_artist:
        return {"success":True,"message":"details fetched succesfully","records": db_artist,"total_records" : len(db_artist)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})