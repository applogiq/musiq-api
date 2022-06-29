from fastapi import APIRouter, Depends,Body,UploadFile,File,Request,HTTPException
import os
from typing import Optional,Union
from sqlalchemy.orm import Session
# from services.sample import song_check

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

@router.post("/songs")
async def enter_song_details(song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return enter_song_detail(db,song,s["sub"])
    
   
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
    
# @router.post("/songs/music/{song_id}")
# async def upload_song_file(song_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     # song = upload_new_song_file(db,song_id,uploaded_file)
#     # return song
#     pass

@router.put("/songs/{song_id}")
async def update_song_details(song_id: int,song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_song(db,song_id,song,s["sub"])
    

@router.delete("/songs/{song_id}")
async def delete_song(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return song_delete(db,song_id)
    

#########------- AUDIO STREAMING ---------#########

@router.get("/audio")
def stream_audio(song_id: str,request: Request,db: Session = Depends(get_db)):
    song = song_get_by_id(db,song_id)
    if song:
        return song_response(db,song_id,request)
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    
#########------- AUDIO STREAMING ---------#########