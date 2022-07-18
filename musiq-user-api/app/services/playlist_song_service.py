from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from model.playlist_song_model import playlist_songs
from model.album_model import albums
from model.song_model import songs
from model.playlist_model import playlist
from services.user_service import *

###enter playlist song details
def playlist_song_detail(db: Session,playlists,email):
    playlistname = db.query(playlist_songs).filter(playlist_songs.playlist_id == playlists.playlist_id,playlist_songs.song_id == playlists.song_id,playlist_songs.is_delete == False).first()
    if playlistname:
        raise HTTPException(status_code=400, detail="This song is already added in this playlist")
    
    temp = db.query(playlist).filter(playlist.id.in_([playlists.playlist_id]),playlist.is_delete == False).first()
    if temp:
        s = temp.no_of_songs 
        temp.no_of_songs = s+1

        temp1 = get_email(email,db)
        db_user = playlist_songs(playlist_id = playlists.playlist_id,
                        song_id = playlists.song_id,
                        is_delete = False,
                        created_by = temp1.id,
                        is_active = True)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    return False

##get all playlistsong details
def playlistsong_get_all(db: Session):
    return db.query(playlist_songs).filter(playlist_songs.is_delete == False).all()

##get particular playlist's song details
def playlistsong_get_by_playlistid(db: Session, id: int):
    return db.query(playlist_songs,playlist.id,playlist.playlist_name,playlist.no_of_songs,songs.song_id,songs.song_name,songs.album_id,albums.album_id,albums.album_name,albums.music_director_name,albums.is_image).join(songs,songs.id==playlist_songs.song_id).join(albums,albums.id == songs.album_id).join(playlist,playlist.id == playlist_songs.playlist_id).filter(playlist_songs.playlist_id == id,playlist_songs.is_delete == False).all()

###get particular playlistsong details
def playlistsong_get_by_id(db: Session, playlist_id: int):
    playlists = db.query(playlist_songs).filter(playlist_songs.id == playlist_id,playlist_songs.is_delete == False).first()
    if playlists:
        return playlists
    else:
        return False

###delete particular song from some playlist
def playlistsong_delete(db: Session,playlist_id):
    user_temp = db.query(playlist_songs).filter(playlist_songs.id == playlist_id,playlist_songs.is_delete == False).first()
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return True
    return False
