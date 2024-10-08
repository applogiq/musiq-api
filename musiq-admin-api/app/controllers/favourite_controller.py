from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.favourite_service import *

###response of adding favourite song for particular user
def favourite_detail(db: Session,fav,email):
    db_fav = fav_song_detail(db,fav,email)
    if db_fav:
        return {"success":True,'message': "song added in favourite list","records": db_fav}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "check your details"})

###response of getting particular user's favourite detail
def get_fav_details_by_userid(db, user_id):
    db_fav = fav_get_by_userid(db, user_id)
    if db_fav:
        return {"success":True,"message":"successfully fetched","records": db_fav,"total_records" : len(db_fav)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})

###response of getting all user's favourite detail
def get_all_fav_song(db):
    try:
        db_fav = fav_get_all(db)
        return {"success":True,"message":"details fetched succesfully","records": db_fav,"total_records" : len(db_fav)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

###response for removing song from from particular user's favourites
def delete_fav_song(db,fav):
    db_fav = fav_delete(db,fav)
    if db_fav:
        return {"status": True,"message":"song removed from favourite list"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "favourite song details doesn't exist"})