from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from model.playlist_song_model import playlist_songs
from model.playlist_model import playlist
from services.admin_user_service import admin_get_email

def playlist_song_detail(db: Session,playlists,email):
    playlistname = db.query(playlist_songs).filter(playlist_songs.playlist_id == playlists.playlist_id,playlist_songs.song_id == playlists.song_id,playlist_songs.is_delete == False).first()
    if playlistname:
        raise HTTPException(status_code=400, detail="This song is already added in this playlist")
    
    temp = db.query(playlist).filter(playlist.id.in_([playlists.playlist_id]),playlist.is_delete == False).first()
    if temp:
        s = temp.no_of_songs 
        temp.no_of_songs = s+1

        temp1 = admin_get_email(email,db)
        db_user = playlist_songs(playlist_id = playlists.playlist_id,
                        song_id = playlists.song_id,
                        is_delete = False,
                        created_by = temp1.id,
                        is_active = True)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message":"data added"}
    return ("Not found")

def playlistsong_get_all(db: Session):
    return db.query(playlist_songs).filter(playlist_songs.is_delete == False).all()

def playlistsong_get_by_playlistid(db: Session, playlist_id: int):
    playlists = db.query(playlist_songs).filter(playlist_songs.playlist_id == playlist_id,playlist_songs.is_delete == False).all()
    if playlists:
        return playlists
    else:
        return False

def playlistsong_get_by_id(db: Session, playlist_id: int):
    playlists = db.query(playlist_songs).filter(playlist_songs.id == playlist_id,playlist_songs.is_delete == False).first()
    if playlists:
        return playlists
    else:
        return False

def playlistsong_delete(db: Session,playlist_id):
    user_temp = db.query(playlist_songs).filter(playlist_songs.id == playlist_id,playlist_songs.is_delete == False).first()
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="playlist details doesn't exist")
