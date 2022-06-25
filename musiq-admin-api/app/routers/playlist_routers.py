from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from services.playlist_service import *
from schemas.playlist_schema import *
from controllers.playlist_controller import *
# from controllers.recent_controller import user_recent_song


router = APIRouter(tags=["playlist"],prefix='/playlist')

http_bearer = JWTBearer()

@router.post("/")
async def enter_playlist_details(playlists:PlaylistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    return create_playlist_details(db,playlists,s["sub"])

@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_playlist(db)

@router.get("/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_playlist_by_id(db,playlist_id)

@router.get("/user/{user_id}")
async def view_user_playlist_details(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_playlist_by_userid(db, user_id)

@router.put("/{playlist_id}")
async def update_playlist_details(playlist_id: int,name: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_playlist(db,playlist_id,name,s["sub"])
   
@router.delete("/{playlist_id}")
async def delete_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_playlist(db,playlist_id)
     
