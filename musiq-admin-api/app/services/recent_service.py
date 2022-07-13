from requests import session
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from model.recent_model import recents
from model.song_model import songs
from services.admin_user_service import admin_get_email
from services.song_service import *

###get recent songs of single user by id
def recent_get_by_userid(db,user_id):
    return db.query(recents).filter(recents.user_id == user_id,recents.is_delete == False).first()

###get all user recent songs detail
def recent_get_all(db):
    return db.query(recents).filter(recents.is_delete == False).all()

###get recent songs of user in order
def recent_song_check(db,user_id):
    user = recent_get_by_userid(db,user_id)
    if user:
        s = list(user.song_id["songs"])
        temp = db.query(songs.id,songs.song_name,albums.album_id,albums.album_name,albums.music_director_name).join(albums,albums.id == songs.album_id).filter(songs.id.in_(s)).all()
        temp2 = temp[::-1]
        return temp2
    return False


###update recent song detail of single user
def recent_update(db,user_id,data,email):
    temp = recent_get_by_userid(db,user_id)
    user = admin_get_email(email,db)
    temp.song_id["songs"] = data
    temp.updated_at = datetime.now()
    temp.updated_by = user.id
    db.commit()
    temp1 = recent_get_by_userid(db,user_id)
    return temp1