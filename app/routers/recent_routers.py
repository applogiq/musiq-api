from fastapi import APIRouter, Depends,HTTPException

from app.auth.auth_bearer import JWTBearer
from app.controller.recent_controller import get_user_song, get_users_songs, user_recent_song
from app.controller.user_controller import get_db
from sqlalchemy.orm import Session
from app.schema.recent_schema import RecentSchema

router = APIRouter()

http_bearer = JWTBearer()


@router.get("/recent", tags=["recents"])
async def view_all_song_details(db: Session = Depends(get_db)):
    # pass
    try:
        users = get_users_songs(db)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"total_records" : s,"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/recent/{user_id}", tags=["recents"])
async def view_song_details(user_id: int,db: Session = Depends(get_db)):
    db_user = get_user_song(db, user_id)
    if db_user:
        return {"records": db_user,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/recent", tags=["recents"])
async def last_song_details(song: RecentSchema,db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    # pass
    user = user_recent_song(db,song)
    if user:
        return user