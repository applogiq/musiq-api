from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from app.model.playlist_model import playlist

def playlist_detail(db: Session,playlists):
    playlistname =db.query(playlist).filter(playlist.name == playlists.name,playlist.user_id == playlists.user_id,playlist.is_delete == 0).first()
    if playlistname:
        raise HTTPException(status_code=400, detail="playlistname is already exist")

    db_user = playlist(name = playlists.name,
                    user_id = playlists.user_id,
                    no_of_songs = 0,
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"data added"}

def get_playlists(db: Session):
    return db.query(playlist).filter(playlist.is_delete == 0).all()

def get_playlist(db: Session, playlist_id: int):
    playlists = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == 0).first()
    if playlists:
        return playlists
    else:
        return False

def playlist_update(db,playlist_id,name):
    user_temp = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == 0).first()
    if user_temp:
        if name:
            user_temp.name = name
        # if playlists.song_id:
        #     user_temp.song_id = playlists.song_id
        
        user_temp.updated_by = 1
        user_temp.updated_at = datetime.now()
        db.commit()
        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="playlist details doesn't exist")

def playlist_delete(db: Session,playlist_id):
    user_temp = db.query(playlist).filter(playlist.id == playlist_id,playlist.is_delete == 0).first()
    if user_temp:
        user_temp.is_delete = 1
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="playlist details doesn't exist")