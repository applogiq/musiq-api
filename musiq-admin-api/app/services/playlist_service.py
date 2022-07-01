from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from model.playlist_model import playlist
from services.playlist_song_service import playlistsong_get_by_playlistid
from services.admin_user_service import admin_get_email

def playlist_detail(db: Session,playlists,email):
    playlistname =db.query(playlist).filter(playlist.playlist_name == playlists.playlist_name,playlist.user_id == playlists.user_id,playlist.is_delete == False).first()
    if playlistname:
        raise HTTPException(status_code=400, detail="playlistname is already exist")
    temp = admin_get_email(email,db)
    db_user = playlist(playlist_name = playlists.playlist_name,
                    user_id = playlists.user_id,
                    no_of_songs = 0,
                    is_delete = False,
                    created_by = temp.id,
                    is_active = True)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def playlist_update(db,playlist_id,name,email):
    user_temp = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == False).first()
    temp = admin_get_email(email,db)
    if user_temp:
        if name:
            user_temp.playlist_name = name
        user_temp.updated_by = temp.id
        user_temp.updated_at = datetime.now()
        db.commit()
        return True
    return False

def playlist_get_all(db: Session):
    return db.query(playlist).filter(playlist.is_delete == False).all()

def playlist_get_by_id(db: Session, playlist_id: int):
    playlists = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == False).first()
    if playlists:
        return playlists
    else:
        return False
    
def playlist_get_by_userid(db: Session, user_id: int):
    playlists = db.query(playlist).filter(playlist.user_id == user_id,playlist.is_delete == False).order_by(playlist.created_by).all()
    s = []
    for i in range(0,len(playlists)):
        if playlists[i].no_of_songs:  
            a = playlistsong_get_by_playlistid(db,playlists[i].id)
            s.append(a[0])
        else:
            a = playlist_get_by_id(db,playlists[i].id)
            s.append(a)    
    return s

# def playlist_get_by_userid(db: Session, user_id: int):
#     playlists = db.query(playlist).filter(playlist.user_id == user_id,playlist.is_delete == False).all()
#     if playlists:
#         return playlists
#     else:
#         return False

def playlist_delete(db: Session,playlist_id):
    user_temp = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == False).first()
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return True
    else:
        return False