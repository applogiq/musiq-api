from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.playlist_service import *

def enter_playlist_details(db: Session,playlists,email):
    db_playlist = playlist_detail(db,playlists,email)
    if db_playlist:
        return {"success":True,"message": "playlist added successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})

def get_all_playlist(db):
    try:
        users = playlist_get_all(db)
        return {"success":True,"message": "details fetched successfully","records": users,"total_records" : len(users)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    
def get_playlist_by_id(db, playlist_id):
    playlists = playlist_get_by_id(db, playlist_id)
    if playlists:
        return {"success":True,"message": "details fetched successfully","records": playlists,"total_records" : len(playlists)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


def get_playlist_by_userid(db, user_id):
    playlists = playlist_get_by_userid(db, user_id)
    if playlists:
        return {"success":True,"message": "details fetched successfully","records": playlists,"total_records" : len(playlists)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

def update_playlist_details(db,playlist_id,name,email):
    playlists = playlist_update(db,playlist_id,name,email)
    if playlists:
        return {"success":True,"message": "playlist updated successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})

def delete_playlist_details(db,playlist_id):
    playlists = playlist_delete(db,playlist_id)
    if playlists:
        return {"success":True,"message": "playlist deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})