from fastapi import APIRouter, Depends,HTTPException


from utils.auth_bearer import JWTBearer
from utils.auth_handler import decodeJWT

from sqlalchemy.orm import Session
from config.database import *
from schemas.last_song_schema import LastSchema
from services.last_song_service import *
# from app.controller.last_song_controller import get_last_song, get_last_songs, user_last_song



router = APIRouter(tags=["last song"],prefix='/last-song')

http_bearer = JWTBearer()


@router.get("/")
async def view_all_last_song_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        users = last_song_get_all(db)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"total_records" : s,"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/{user_id}")
async def view_user_last_song_details(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    pass
    db_user = last_song_get_by_userid(db, user_id)
    if db_user:
        return {"records": db_user,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/")
async def last_song_details(song: LastSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    user = user_last_song(db,song,s["sub"])
    if user:
        return user

@router.get("/{last-song-id}")
async def view_last_song_detail(last_song: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    pass
 