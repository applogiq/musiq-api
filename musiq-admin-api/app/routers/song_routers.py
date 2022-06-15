from fastapi import APIRouter, Depends,Body,UploadFile,File,Request,HTTPException
import os
from model.album_model import albums
from typing import Optional
from sqlalchemy.orm import Session

# from controllers.user_controller import *
from schemas.song_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *
from services.song_service import *

router = APIRouter(tags=["songs"])

http_bearer = JWTBearer()

@router.post("/songs")
async def enter_song_details(song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = song_detail(db,song)
    if user:
        return {'message': "song details added","success":True}
    else:
        return {'message': "Check your details","success": False}
    # pass

@router.get("/songs",response_model=AllresponseSchema)
async def view_all_song_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    # try:
    #     users = get_songs(db, skip=skip, limit=limit)
    #     return {"records": users,"totalrecords" : len(users),"success":True}
    # except:
    #     raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    pass

@router.get("/songs/{song_id}",response_model=SongresponseSchema)
async def view_song_details(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # db_user = get_song(db, song_id)
    # if db_user:
    #     return {"records": db_user,"totalrecords" : 1,"success":True}
    # else:
    #     raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
    pass

@router.put("/songs/{song_id}")
async def update_song_details(song_id: int,song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # temp = song_update(db,song_id,song)
    # return temp
    pass

@router.delete("/songs/{song_id}")
async def delete_song(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # song = delete_song_details(db,song_id)
    # return song
    pass

#########------- AUDIO STREAMING ---------#########

@router.get("/audio")
def stream_audio(song_id: str,request: Request,db: Session = Depends(get_db)):
    # user_temp = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    # if user_temp:
    #     temp = db.query(albums).filter(albums.album_id == user_temp.album_id,albums.is_delete == 0).first()
    #     if temp.name[0].isalpha():
    #         alphabet = temp.name[0].upper()
    #     else:
    #         alphabet = "Mis" 
    #     file_location = f"public/music/tamil/{alphabet}/{temp.name}/songs/{user_temp.song_id}.wav"
    #     return range_requests_response(
    #         request, file_path=file_location, content_type="audio/wav" 
    #     )
    # else:
    #     raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    pass

#########------- AUDIO STREAMING ---------#########