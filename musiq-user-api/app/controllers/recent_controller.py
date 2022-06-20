from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.recent_service import *



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
        raise HTTPException(status_code=404, detail="check your id!!!")
