from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from services.playlist_song_service import *
from schemas.playlist_song_schema import *


router = APIRouter(tags=["playlist songs"],prefix='/playlist-song')

http_bearer = JWTBearer()

@router.post("/")
async def enter_aura_details(playlists:PlaylistsongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    playlist_song = playlist_song_detail(db,playlists,s["sub"])
    return playlist_song

@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        users = playlistsong_get_all(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/{id}")
async def view_playlist_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    playlists = playlistsong_get_by_id(db,id)
    if playlists:
        return {"records": playlists,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
    

@router.get("/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    playlists = playlistsong_get_by_playlistid(db, playlist_id)
    if playlists:
        return {"records": playlists,"total_records" :len(playlists),"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


@router.delete("/{id}")
async def delete_playlist_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = playlistsong_delete(db,id)
    return temp