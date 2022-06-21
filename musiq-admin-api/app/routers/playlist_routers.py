from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from services.playlist_service import *
from schemas.playlist_schema import *
# from controllers.recent_controller import user_recent_song



router = APIRouter(tags=["playlist"],prefix='/playlist')

http_bearer = JWTBearer()

@router.post("/")
async def enter_playlist_details(playlists:PlaylistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    playlist = playlist_detail(db,playlists,s["sub"])
    return playlist

@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    try:
        users = playlist_get_all(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    

@router.get("/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db)):
    playlists = playlist_get_by_id(db, playlist_id)
    if playlists:
        return {"records": playlists,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/user/{user_id}")
async def view_user_playlist_details(user_id: int,db: Session = Depends(get_db)):
    playlists = playlist_get_by_userid(db, user_id)
    if playlists:
        return {"records": playlists,"total_records" : len(playlists),"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/{playlist_id}")
async def update_playlist_details(playlist_id: int,name: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    temp = playlist_update(db,playlist_id,name,s["sub"])
    return temp
   
@router.delete("/{playlist_id}")
async def delete_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = playlist_delete(db,playlist_id)
    return temp
