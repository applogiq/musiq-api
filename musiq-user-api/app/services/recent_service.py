from requests import session
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from model.recent_model import recents
from model.song_model import songs
from services.user_service import *
from services.song_service import *

###get recent songs of single user by id
def recent_get_by_userid(db,user_id):
    return db.query(recents).filter(recents.user_id == user_id,recents.is_delete == False).first()

###get all user recent songs detail
def recent_get_all(db):
    return db.query(recents).filter(recents.is_delete == False).all()

###get recent songs of user in order
def recent_song_check(db,user_id,limit):
    user = recent_get_by_userid(db,user_id)
    if user:
        s = list(user.song_id["songs"])
        print(s)
        # temp = db.query(recents).filter(songs.id.in_(s)).limit(limit).all()
        temp2 = []
        for i in s:
            temp = db.query(songs.id,songs.song_name,songs.duration,albums.album_id,albums.album_name,albums.music_director_name).join(albums,albums.id == songs.album_id).filter(songs.id == i).limit(limit).all()
            temp2.append(temp)
        temp2 = temp2[::-1]
        return temp2
    return False

###update recent song detail of single user
def recent_update(db,song,email):#data
    user_temp = recent_get_by_userid(db,song.user_id)
    if user_temp:
        if song_get_by_id(db,song.song_id):
            temp = []
            if len(user_temp.song_id["songs"]):
                temp = list(user_temp.song_id["songs"])
            if len(user_temp.song_id["songs"]) > 1:
                count = len(user_temp.song_id["songs"])
            else:
                count = 1
            if count == 30:  
                if song.song_id in temp:
                    for i in range(0,count):
                        if i < len(user_temp.song_id["songs"]):
                            if song.song_id == temp[i]:
                                temp.pop(i)
                                temp.append(song.song_id)
                else:
                    temp.pop(0)
                    temp.append(song.song_id)
            elif count < 30:
                if song.song_id in temp:
                    for i in range(0,count):
                        if i < len(user_temp.song_id["songs"]):
                            if song.song_id == temp[i]:
                                temp.pop(i)
                                temp.append(song.song_id)
                else:
                    temp.append(song.song_id)

            db_recent = recent_get_by_userid(db,song.user_id)
            user = get_email(email,db)
            db_recent.song_id["songs"] = temp
            db_recent.updated_at = datetime.now()
            db_recent.updated_user_by = user.id
            db.commit()
            response = recent_get_by_userid(db,song.user_id)
            return response
    return False