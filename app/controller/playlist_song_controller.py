from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from app.model.playlist_song_model import playlist_songs
from app.model.playlist_model import playlist

def playlist_song_detail(db: Session,playlists):
    playlistname =db.query(playlist_songs).filter(playlist_songs.playlist_id == playlists.playlist_id,playlist_songs.song_id == playlists.song_id,playlist_songs.is_delete == 0).first()
    if playlistname:
        raise HTTPException(status_code=400, detail="This song is already added in this playlist")
    
    temp = db.query(playlist).filter(playlist.id == playlists.playlist_id,playlist.is_delete == 0).first()
    s = temp.no_of_songs 
    temp.no_of_songs = s+1

    db_user = playlist_songs(playlist_id = playlists.playlist_id,
                    song_id = playlists.song_id,
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message":"data added"}

def get_playlistsongs(db: Session):
    return db.query(playlist_songs).filter(playlist_songs.is_delete == 0).all()

def get_playlistsong(db: Session, playlist_id: int):
    playlists = db.query(playlist_songs).filter(playlist_songs.id == playlist_id,playlist_songs.is_delete == 0).first()
    if playlists:
        return playlists
    else:
        return False

def playlistsong_delete(db: Session,playlist_id):
    user_temp = db.query(playlist_songs).filter(playlist_songs.id == playlist_id,playlist_songs.is_delete == 0).first()
    if user_temp:
        user_temp.is_delete = 1
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="playlist details doesn't exist")
