from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from services.playlist_song_service import *
from schemas.playlist_song_schema import *
from controllers.playlist_song_controller import *


router = APIRouter(tags=["playlist songs"],prefix='/playlist-song')

http_bearer = JWTBearer()

@router.post("/")
async def enter_playlist_song_details(playlists:PlaylistsongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    playlist_song = create_playlist_song(db,playlists,s["sub"])
    return playlist_song

@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_playlist_song(db)

@router.get("/{id}")
async def view_playlist_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_playlist_song_by_id(db,id)
    

@router.get("/list/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_song_by_playlist_id(db, playlist_id)
    

@router.delete("/{id}")
async def delete_playlist_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_playlistsong(db,id)

