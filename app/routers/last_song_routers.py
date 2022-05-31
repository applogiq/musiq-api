from fastapi import APIRouter, Depends,Body,UploadFile,File,Request,HTTPException
import os
from app.controller.last_song_controller import get_last_song, get_last_songs, user_last_song
from app.model.album_model import albums

from app.schema.last_song_schema import LastSchema
from app.model.last_song_model import last_songs
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from sqlalchemy.orm import Session

router = APIRouter()

http_bearer = JWTBearer()

@router.put("/lasts", tags=["last song"])
async def last_song_details(song: LastSchema,db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    user = user_last_song(db,song)
    if user:
        return user
    # pass


@router.get("/lasts", tags=["last song"])
async def view_all_song_details(db: Session = Depends(get_db)):
    try:
        users = get_last_songs(db)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"total_records" : s,"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/lasts/{user_id}", tags=["last song"])
async def view_song_details(user_id: int,db: Session = Depends(get_db)):
    db_user = get_last_song(db, user_id)
    if db_user:
        return {"records": db_user,"total_records" : 1,"sucess":True}
    else:
        # return {"message": "couldn't fetch,check your id","sucess":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
 

# @router.put("/lasts/{song_id}", tags=["last song"])
# async def update_song_details(song_id: int,song: LastSchema,db: Session = Depends(get_db)):
#     pass

# @router.delete("/lasts/{song_id}", tags=["last song"])
# async def delete_song(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     pass
    

