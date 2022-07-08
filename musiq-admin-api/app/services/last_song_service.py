from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from model.last_song_model import last_songs
from model.song_model import songs
from services.admin_user_service import admin_get_email
from services.song_service import *

def last_song_get_by_userid(db: Session, user_id: int):
    return db.query(last_songs).filter(last_songs.user_id == user_id,last_songs.is_delete == False).first()

def last_song_get_all(db):
    return db.query(last_songs).filter(last_songs.is_delete == False).all()

# def last_song_get_by_id(db:Session,id):
#     return db.query(last_songs).filter(last_songs.id == id,last_songs.is_delete == False).first()

def user_last_song(db: Session,song,email):
    user_temp = last_song_get_by_userid(db,song.user_id)
    if user_temp:
        song_temp = song_get_by_id(db,song.song_id)
        temp = admin_get_email(email,db)
        user_temp.song_id = song.song_id
        user_temp.duration = song_temp.duration
        user_temp.paused_timing = song.paused_timing
        user_temp.updated_at = datetime.now()
        user_temp.updated_by = temp.id
        if song.paused_timing >= "00:01:00":
            s = song_temp.listeners
            if s:
                pass
            else:
                s = 0
            song_temp.listeners = s+1
        else:
            pass
        db.commit()
        return True
    return False