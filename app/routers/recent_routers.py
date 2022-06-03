from fastapi import APIRouter, Depends,HTTPException

from app.auth.auth_bearer import JWTBearer
from app.controller.recent_controller import get_user_song, get_users_songs, user_recent_song
from app.controller.user_controller import get_db
from sqlalchemy.orm import Session
from app.schema.recent_schema import RecentSchema,AllrecentSchema,RecentresponseSchema

router = APIRouter(tags=["recents"],prefix='/recent')

http_bearer = JWTBearer()


@router.get("/",response_model=AllrecentSchema)
async def view_all_song_details(db: Session = Depends(get_db)):
    # pass
    try:
        users = get_users_songs(db)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"totalrecords" : s,"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/{user_id}",response_model=RecentresponseSchema)
async def view_song_details(user_id: int,db: Session = Depends(get_db)):
    db_user = get_user_song(db, user_id)
    if db_user:
        return {"records": db_user,"totalrecords" : 1,"success":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/")
async def last_song_details(song: RecentSchema,db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    # pass
    user = user_recent_song(db,song)
    if user:
        return user