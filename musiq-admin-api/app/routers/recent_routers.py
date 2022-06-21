from fastapi import APIRouter, Depends,HTTPException

from utils.auth_bearer import JWTBearer

from sqlalchemy.orm import Session
from config.database import *
from utils.auth_handler import decodeJWT
from services.recent_service import *
from schemas.recent_schema import RecentSchema,AllrecentSchema,RecentresponseSchema
from controllers.recent_controller import user_recent_song

router = APIRouter(tags=["recents"],prefix='/recent-list')

http_bearer = JWTBearer()


@router.get("/",response_model=AllrecentSchema)
async def view_all_song_details(db: Session = Depends(get_db)):
    # pass
    try:
        users = recent_get_all(db)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"totalrecords" : s,"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/{user_id}")#,response_model=RecentresponseSchema
async def view_song_details(user_id: str,db: Session = Depends(get_db)):
    # pass
    db_user = recent_song_check(db,user_id)
    if db_user:
        return db_user
    #     return {"records": db_user,"totalrecords" : 1,"success":True}
    # else:
    #     raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/")
async def last_song_details(song: RecentSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):#
    # pass
    s = decodeJWT(token)
    user = user_recent_song(db,song,s["sub"])
    if user:
        return user