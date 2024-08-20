from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from services.playlist_service import *
from schemas.playlist_schema import *
from controllers.playlist_controller import *

router = APIRouter(tags=["playlist"],prefix='/playlist')

http_bearer = JWTBearer()

###enter new playlist detail for particular user
@router.post("/")
async def enter_playlist_details(playlists:PlaylistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    return create_playlist_details(db,playlists,s["sub"])

###to get all user's playlist details
@router.get("/")
async def view_all_playlist_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_playlist(db)

###to get particular playlist details
@router.get("/{playlist_id}")
async def view_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_playlist_by_id(db,playlist_id)

###to get particular user's all playlist song details
@router.get("/user/{user_id}")
async def view_user_playlist_details(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_playlist_by_userid(db, user_id)

###to update existing playlist details
@router.put("/{playlist_id}")
async def update_playlist_details(playlist_id: int,playlists: UpdateSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_playlist(db,playlist_id,playlists.name,s["sub"])
   
###to delete entire playlist details by their id
@router.delete("/{playlist_id}")
async def delete_playlist_details(playlist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return delete_playlist(db,playlist_id,s["sub"])
     
