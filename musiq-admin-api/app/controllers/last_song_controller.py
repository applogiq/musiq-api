from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.last_song_service import *

###all user's last song details response
def get_all_last_song_details(db):
    try:
        last_song = last_song_get_all(db)
        return {"success":True,"message": "details fetched successfully","records": last_song,"total_records" : len(last_song)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    
###particular user's last jeard song details response
def get_details_by_userid(db, user_id):
    last_song = last_song_get_by_userid(db, user_id)
    if last_song:
        return {"success":True,"message": "details fetched successfully","records": last_song,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

####response of updating last heard song of particular user
def enter_last_song(db: Session,song,email):
    last_song = user_last_song(db,song,email)
    if last_song:
        return {"success":True,"message": "song updated successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})




