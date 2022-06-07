from fastapi import APIRouter, Depends,Body,UploadFile,File,Request,HTTPException
import os
from app.model.album_model import albums
from typing import Optional

from app.schema.song_schema import SongSchema,SongresponseSchema,AllresponseSchema,SongnewSchema
from app.model.song_model import songs
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from sqlalchemy.orm import Session
from app.controller.song_controller import get_song, get_songs, song_new_detail,song_update,song_detail,delete_song_details
from app.controller.song_controller import upload_new_song_file,upload_base64_song_file,range_requests_response

router = APIRouter(tags=["songs"])

http_bearer = JWTBearer()

# templates = Jinja2Templates(directory=os.path.abspath(os.path.expanduser('templates')))

@router.post("/songs/new")
async def enter_song_details(song: SongnewSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = song_new_detail(db,song)
    if user:
        return {'message': "song details added","success":True}
    else:
        return {'message': "Check your details","success": False}

@router.post("/songs")
async def enter_song_details(song: SongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = song_detail(db,song)
    if user:
        return {'message': "song details added"}
    else:
        return {'message': "couldn't fetch"}

@router.post("/songs/music/{song_id}")
async def upload_song_file(song_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    song = upload_new_song_file(db,song_id,uploaded_file)
    return song
       
@router.post("/songs/music-base64/{song_id}")
async def upload_b64_song_file(song_id: str,song: str = Body(...) ,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    song = upload_base64_song_file(db,song_id,song)
    return song 

@router.get("/songs",response_model=AllresponseSchema)
async def view_all_song_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    try:
        users = get_songs(db, skip=skip, limit=limit)
        return {"records": users,"totalrecords" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/songs/{song_id}",response_model=SongresponseSchema)
async def view_song_details(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_user = get_song(db, song_id)
    if db_user:
        return {"records": db_user,"totalrecords" : 1,"success":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/songs/{song_id}")
async def update_song_details(song_id: int,song: SongnewSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = song_update(db,song_id,song)
    return temp

@router.delete("/songs/{song_id}")
async def delete_song(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    song = delete_song_details(db,song_id)
    return song
    

#########------- AUDIO STREAMING ---------#########

@router.get("/audio")
def stream_audio(song_id: str,request: Request,db: Session = Depends(get_db)):
    user_temp = db.query(songs).filter(songs.id == song_id,songs.is_delete == 0).first()
    if user_temp:
        temp = db.query(albums).filter(albums.album_id == user_temp.album_id,albums.is_delete == 0).first()
        if temp.name[0].isalpha():
            alphabet = temp.name[0].upper()
        else:
            alphabet = "Mis" 
        file_location = f"public/music/tamil/{alphabet}/{temp.name}/songs/{user_temp.song_id}.wav"
        return range_requests_response(
            request, file_path=file_location, content_type="audio/wav" 
        )
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 

#########------- AUDIO STREAMING ---------#########