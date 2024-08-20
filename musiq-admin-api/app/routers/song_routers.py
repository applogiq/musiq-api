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

###to enter song details with base64
@router.post("/songs")
async def enter_song_details(song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return enter_song_detail(db,song,s["sub"])

###to enter details alone without music
@router.post("/new/songs")
async def enter_song_details(song: SongNewSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return enter_new_song_detail(db,song,s["sub"])
    
###to upload music file by it's id
@router.post("/songs/{id}")
async def enter_song(id: int,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return music_upload_details(db,id,file)
    

###to get all song details 
@router.get("/songs")
async def view_all_song_details(db: Session = Depends(get_db),album_id: Union[int, None] = None,artist_id:Union[int, None] = None,skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    if album_id:
        return album_song_check(db,album_id,skip,limit) ###fetch songs from particular album
    elif artist_id:
        return artist_song_check(db,artist_id,skip,limit) ###fetch particular artist songs
    else:
        return get_all_song(db, skip,limit) ###fetch all


###to get particular song details by it's id
@router.get("/songs/{song_id}")
async def view_song_details(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_song_by_id(db, song_id)
    
# @router.post("/songs/music/{song_id}")
# async def upload_song_file(song_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     # song = upload_new_song_file(db,song_id,uploaded_file)
#     # return song
#     pass

###to update existing  song details
@router.put("/songs/{song_id}")
async def update_song_details(song_id: int,song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_song(db,song_id,song,s["sub"])
    
###to delete particular song details by their id
@router.delete("/songs/{song_id}")
async def delete_song(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return song_delete(db,song_id)
    
###to get trending hits of all song
@router.get("/trending-hits")
async def trending_hits_details(limit:int = 100,db: Session = Depends(get_db),token: str = Depends(http_bearer)):#,token: str = Depends(http_bearer)
    return get_trending_hits(db,limit)

###to get new release songs by its release date
@router.get("/new_release")
async def new_release_details(limit: int = 100,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_new_release(db,limit)

#########------- AUDIO STREAMING ---------#########

@router.get("/audio")
def stream_audio(song_id: str,request: Request,db: Session = Depends(get_db)):
    song = song_get_by_id(db,song_id)
    if song:
        return song_response(db,song_id,request)
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    
#########------- AUDIO STREAMING ---------#########


###search functionality
@router.get("/search")
async def search_function(data: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return search_engine_details(db,data)