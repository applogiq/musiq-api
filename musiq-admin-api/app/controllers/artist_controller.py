from fastapi import HTTPException
import re

from services.artist_service import *

###response of creating artist detail
def create_artist_detail(db,artists,email):
    db_artist = artist_detail(db,artists,email) 
    if db_artist:
        return {"success": True,"message":"artist details added","records":db_artist}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "artist details doesn't exist"})

###response of updating existing artist detail
def update_artist(db,id,artists,email):
    db_artist = artist_update(db,id,artists,email)
    if db_artist:
        return {"success": True,"message":"artist details updated Successfully","records":db_artist}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "artist details doesn't exist"})

###response of removing image from particular artist detail
def artist_delete_image(db,artist_id):
    if artist_remove_image(db,artist_id):
        return {"success":True,'message': "artist image removed"}
    else:
        raise HTTPException(status_code=404, detail={"success":False,'message': "Check your id"})

###response of getting all artist details
def get_all_artist_detail(db):
    db_artist = artist_get_all(db)
    if db_artist:
        return {"success":True,"message":"details fetched succesfully","records": db_artist,"total_records" : len(db_artist)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

###response of fetching detail of particular artist
def get_artist_detail_by_id(db,artist_id):
    db_artist = artist_get_by_id(db,artist_id)
    if db_artist:
        return {"success":True,"message":"details fetched succesfully","records": db_artist,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

####response of search engine
def artist_search_engine_details(db,data):
    db_song = artist_search_engine(db,data)
    if db_song:
        return {"success":True,"message":"Song details fetched successfully","records": db_song,"totalrecords" : len(db_song)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})