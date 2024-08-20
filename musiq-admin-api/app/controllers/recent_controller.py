from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.recent_service import *


###response of all user's recent list of songs
def get_all_recent(db):
    try:
        users = recent_get_all(db)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"success":True,"message": "fetched successfully","records": users,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})


###response of single user's recent list of songs
def get_recent_song_list(db,user_id):
    db_user = recent_song_check(db,user_id)
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
    user_temp = recent_get_by_userid(db,song.user_id)
    if user_temp:
        temp = []
        if len(user_temp.song_id["songs"]):
            temp = list(user_temp.song_id["songs"])
        if len(user_temp.song_id["songs"]) > 1:
            s = len(user_temp.song_id["songs"])
        else:
            s = 1
        if s == 30:  
            if song.song_id in temp:
                for i in range(0,s):
                    if i < len(user_temp.song_id["songs"]):
                        if song.song_id == temp[i]:
                            temp.pop(i)
                            temp.append(song.song_id)
            else:
                temp.pop(0)
                temp.append(song.song_id)
        elif s < 30:
            if song.song_id in temp:
                for i in range(0,s):
                    if i < len(user_temp.song_id["songs"]):
                        if song.song_id == temp[i]:
                            temp.pop(i)
                            temp.append(song.song_id)
            else:
                temp.append(song.song_id)

        update = recent_update(db,song.user_id,temp,email) 
        if update:
            return {"status": True,"message":"song added","records":update}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "check your id"})
