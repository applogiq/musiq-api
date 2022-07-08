from fastapi import APIRouter, Depends,HTTPException

from utils.auth_bearer import JWTBearer

from sqlalchemy.orm import Session
from config.database import *
from utils.auth_handler import decodeJWT
from services.recent_service import *
from schemas.recent_schema import RecentSchema,AllrecentSchema,RecentresponseSchema
from controllers.recent_controller import *

router = APIRouter(tags=["recents"],prefix='/recent-list')

http_bearer = JWTBearer()

@router.get("/",response_model=AllrecentSchema)
async def view_all_user_recent_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_recent(db)

@router.get("/{user_id}")#,response_model=RecentresponseSchema
async def view_user_recent_details(user_id: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_recent_song_list(db,user_id)

@router.put("/")
async def recent_song_details(song: RecentSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):#
    s = decodeJWT(token)
    return user_recent_song(db,song,s["sub"])
