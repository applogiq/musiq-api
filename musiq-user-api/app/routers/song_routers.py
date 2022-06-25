from fastapi import APIRouter, Depends,Body,UploadFile,File,Request,HTTPException
import os
from typing import Optional,Union
from sqlalchemy.orm import Session


# from controllers.user_controller import *
from schemas.song_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *
from services.song_service import *
from utils.auth_handler import *
from model.album_model import albums
from controllers.song_controller import *

router = APIRouter(tags=["songs"])

http_bearer = JWTBearer()


@router.get("/songs")#,response_model=AllresponseSchema
async def view_all_song_details(db: Session = Depends(get_db),album_id: Union[int, None] = None,artist_id:Union[int, None] = None,skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    if album_id:
        return album_song_check(db,album_id,skip,limit)
    elif artist_id:
        return artist_song_check(db,artist_id,skip,limit)    
    else:
        return get_all_song(db, skip,limit)

@router.get("/songs/{song_id}")
async def view_song_details(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_song_by_id(db, song_id)

# @router.get("/songs/{song_id}",response_model=SongresponseSchema)
# async def view_song_details(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     # song_check(db,song_id)
#     db_user = song_get_by_id(db, song_id)
#     if db_user:
#         return {"records": db_user,"totalrecords" : 1,"success":True,"message":"Song details fetched successfully"}
#     else:
#         raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

#########------- AUDIO STREAMING ---------#########

@router.get("/audio")
def stream_audio(song_id: str,request: Request,db: Session = Depends(get_db)):
    song = song_get_by_id(db,song_id)
    if song:
        return song_response(db,song_id,request)
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    
#########------- AUDIO STREAMING ---------#########