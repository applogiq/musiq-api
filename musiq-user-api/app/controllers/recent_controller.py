from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.recent_service import *

###response of single user's recent list of songs
def get_recent_song_list(db,user_id,limit):
    db_user = recent_song_check(db,user_id,limit)
    if db_user:
        if len(db_user):
            s = len(db_user)
        else:
            s = 1
        return {"success":True,"message": "fetched successfully","records": db_user,"totalrecords" : s}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch...check your id"})

###response of entering songs in recent list for particular list
def user_recent_song(db: Session,song,email):

    update = recent_update(db,song,email)
    if update:
        return {"status": True,"message":"song added","records":update}
    else:
        raise HTTPException(status_code=404, detail={"message":"check your detail","success":False})
