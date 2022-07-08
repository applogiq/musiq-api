from fastapi import HTTPException
import re

from services.artist_service import *

def create_artist_detail(db,artists,email):
    db_artist = artist_detail(db,artists,email) 
    if db_artist:
        return {"success": True,"message":"aura details deleted","records":db_artist}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "aura details doesn't exist"})

def update_artist(db,id,artists,email):
    db_artist = artist_update(db,id,artists,email)
    if db_artist:
        return {"success": True,"message":"aura details updated Successfully","records":db_artist}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "aura details doesn't exist"})

def artist_delete_image(db,artist_id):
    if artist_remove_image(db,artist_id):
        return {"success":True,'message': "artist image removed"}
    else:
        raise HTTPException(status_code=404, detail={"success":False,'message': "Check your id"})

def get_all_artist_detail(db):
    db_artist = artist_get_all(db)
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
