from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.playlist_song_service import *

###response of  adding song in  particular playlist
def create_playlist_song(db: Session,playlists,email):
    db_playlist = playlist_song_detail(db,playlists,email)
    if db_playlist:
        return {"success":True,"message": "song added successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})

###response of getting particular song from particular playlist
def get_playlist_song_by_id(db,id):
    playlists = playlistsong_get_by_id(db,id)
    if playlists:
        return {"success":True,"message":"details fetched successfully","records": playlists,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

###response of getting list of songs of particular playlist
def get_song_by_playlist_id(db, playlist_id):
    playlists = playlistsong_get_by_playlistid(db, playlist_id)
    if playlists:
        return {"success":True,"message" : "fetched successfully","records": playlists,"total_records" :len(playlists)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

###response for removing song from particular playlist
def delete_playlistsong(db: Session,playlist_id):
    db_song = playlistsong_delete(db,playlist_id)
    if db_song:
        return {"success":True,"message": "song deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your id","success":False})
