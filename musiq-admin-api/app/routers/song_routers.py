from fastapi import APIRouter, Depends,Body,UploadFile,File,Request,HTTPException
import os
from typing import Optional,Union
from sqlalchemy.orm import Session
from services.sample import song_check

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
    user = song_detail(db,song,s["sub"])
    if user:
        return {"success":True,'message': "song details added","records": user}
    else:
        return {'message': "Check your details","success": False}
    # pass

@router.get("/songs")#,response_model=AllresponseSchema
async def view_all_song_details(db: Session = Depends(get_db),album_id: Union[int, None] = None,artist_id:Union[int, None] = None,skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    if album_id:
        users = song_album_check(db,album_id,skip,limit)
        # print(user)
    elif artist_id:
        users = song_artist_check(db,artist_id,skip,limit)
    else:
        users = song_get_all(db, skip,limit)
    if users:
        return {"success":True,"message":"Song details fetched successfully","records": users,"totalrecords" : len(users)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/songs/{song_id}",response_model=SongresponseSchema)
async def view_song_details(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # song_check(db,song_id)
    db_user = song_get_by_id(db, song_id)
    if db_user:
        return {"records": db_user,"totalrecords" : 1,"success":True,"message":"Song details fetched successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


@router.put("/songs/{song_id}")
async def update_song_details(song_id: int,song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    temp = song_update(db,song_id,song,s["sub"])
    return temp

@router.delete("/songs/{song_id}")
async def delete_song(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    song = delete_song_details(db,song_id)
    return song
    # pass

#########------- AUDIO STREAMING ---------#########

@router.get("/audio")
def stream_audio(song_id: str,request: Request,db: Session = Depends(get_db)):
    song = song_get_by_id(db,song_id)
    if song:
        return song_response(db,song_id,request)
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    
#########------- AUDIO STREAMING ---------#########