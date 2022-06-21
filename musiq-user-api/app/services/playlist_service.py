from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from model.playlist_model import playlist
from services.user_service import get_email

def playlist_detail(db: Session,playlists,email):
    playlistname =db.query(playlist).filter(playlist.playlist_name == playlists.playlist_name,playlist.user_id == playlists.user_id,playlist.is_delete == False).first()
    if playlistname:
        raise HTTPException(status_code=400, detail="playlistname is already exist")
    temp = get_email(email,db)
    db_user = playlist(playlist_name = playlists.playlist_name,
                    user_id = playlists.user_id,
                    no_of_songs = 0,
                    is_delete = False,
                    created_user_by = temp.id,
                    is_active = True)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"status": True,"message":"playlist is added successfully","records":db_user}

def playlist_update(db,playlist_id,name,email):
    user_temp = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == False).first()
    temp = get_email(email,db)
    if user_temp:
        if name:
            user_temp.playlist_name = name
        # if playlists.song_id:
        #     user_temp.song_id = playlists.song_id
        
        user_temp.updated_user_by = temp.id
        user_temp.updated_at = datetime.now()
        db.commit()
        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="playlist details doesn't exist")

# def playlist_get_all(db: Session):
#     return db.query(playlist).filter(playlist.is_delete == False).all()

def playlist_get_by_id(db: Session, playlist_id: int):
    playlists = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == False).first()
    if playlists:
        return playlists
    else:
        return False
    

def playlist_get_by_userid(db: Session, user_id: int):
    playlists = db.query(playlist).filter(playlist.user_id == user_id,playlist.is_delete == False).all()
    if playlists:
        return playlists
    else:
        return False

def playlist_delete(db: Session,playlist_id):
    user_temp = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == False).first()
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return {"message":"playlist details deleted"}
    else:
        raise HTTPException(status_code=404, detail="playlist details doesn't exist")