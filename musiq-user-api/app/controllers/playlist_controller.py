from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.playlist_service import *

def create_playlist_details(db: Session,playlists,email):
    db_playlist = playlist_detail(db,playlists,email)
    if db_playlist:
        return {"success":True,"message": "playlist added successfully","records":db_playlist,"total_records": len(db_playlist)}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})
    
def get_playlist_by_id(db, playlist_id):
    playlists = playlist_get_by_id(db, playlist_id)
    if playlists:
        return {"success":True,"message": "details fetched successfully","records": playlists,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


def get_playlist_by_userid(db, user_id):
    playlists = playlist_get_by_userid(db, user_id)
    if playlists:
        return {"success":True,"message": "details fetched successfully","records": playlists,"total_records" : len(playlists)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

def update_playlist(db,playlist_id,name,email):
    playlists = playlist_update(db,playlist_id,name,email)
    if playlists:
        return {"success":True,"message": "playlist updated successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})

def delete_playlist(db,playlist_id,email):
    db_playlist = playlist_delete(db,playlist_id,email)
    if db_playlist:
        return {"success":True,"message": "playlist added successfully","records":db_playlist,"total_records": len(db_playlist)}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})