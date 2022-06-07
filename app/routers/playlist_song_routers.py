from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from app.auth.auth_bearer import JWTBearer
from app.controller.playlist_controller import playlist_detail
from app.controller.playlist_song_controller import get_playlistsong, get_playlistsongs, playlist_song_detail, playlistsong_delete
from app.controller.user_controller import get_db
from app.schema.playlist_song_schema import PlaylistsongSchema

router = APIRouter(tags=["playlist songs"],prefix='/playlist-song')

http_bearer = JWTBearer()

@router.post("/")
async def enter_aura_details(playlists:PlaylistsongSchema,db: Session = Depends(get_db)): 
    # pass
    aura = playlist_song_detail(db,playlists)
    return aura

@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    try:
        users = get_playlistsongs(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    

@router.get("/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db)):
    playlists = get_playlistsong(db, playlist_id)
    if playlists:
        return {"records": playlists,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


@router.delete("/{playlist_id}")
async def delete_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = playlistsong_delete(db,playlist_id)
    return temp