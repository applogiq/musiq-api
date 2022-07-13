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

###enter song details for particular playlist detail
@router.post("/")
async def enter_playlist_song_details(playlists:PlaylistsongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    playlist_song = create_playlist_song(db,playlists,s["sub"])
    return playlist_song

###get all user's all playlist song details
@router.get("/")
async def view_all_playlist_song_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_playlist_song(db)

###to get particular playlist song details
@router.get("/{id}")
async def view_playlist_song_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_playlist_song_by_id(db,id)
    
###to get song detail of particular playlist list
@router.get("/list/{playlist_id}")
async def list_playlist_song_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_song_by_playlist_id(db, playlist_id)
    
###to delete song from particular playlist
@router.delete("/{id}")
async def delete_playlist_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_playlistsong(db,id)

