from fastapi import APIRouter, Depends,HTTPException

from utils.auth_bearer import JWTBearer
from utils.auth_handler import decodeJWT

from sqlalchemy.orm import Session
from config.database import *
from schemas.last_song_schema import LastSchema
from services.last_song_service import *
from controllers.last_song_controller import *

router = APIRouter(tags=["last song"],prefix='/last-song')

http_bearer = JWTBearer()


@router.get("/{user_id}")
async def view_user_last_song_details(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_details_by_userid(db, user_id)

@router.put("/")
async def last_song_details(song: LastSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return enter_last_song(db,song,s["sub"])

 