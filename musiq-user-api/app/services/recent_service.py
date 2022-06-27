from requests import session
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from model.recent_model import recents
from model.song_model import songs
from services.user_service import *
from services.song_service import *

def recent_get_by_userid(db,user_id):
    return db.query(recents).filter(recents.user_id == user_id,recents.is_delete == False).first()

def recent_get_all(db):
    return db.query(recents).filter(recents.is_delete == False).all()

def recent_song_check(db,user_id,limit):
    user = recent_get_by_userid(db,user_id)
    if user:
        s = list(user.song_id["songs"])
        temp = db.query(songs.id,songs.song_name,albums.album_id,albums.album_name,albums.music_director_name).join(albums,albums.id == songs.album_id).filter(songs.id.in_(s)).limit(limit).all()
        temp2 = temp[::-1]
        return temp2
    return False

def recent_update(db,user_id,data,email):
    temp = recent_get_by_userid(db,user_id)
    user = get_email(email,db)
    temp.song_id["songs"] = data
    temp.updated_at = datetime.now()
    temp.updated_user_by = user.id
    db.commit()
    temp1 = recent_get_by_userid(db,user_id)
    return temp1