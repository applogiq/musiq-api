from fastapi import APIRouter, Depends,UploadFile,File,Request,Body,Query,HTTPException
from pydantic import Required
from typing import Union,List
from sqlalchemy.orm import Session
from app.controller.album_controller import album_delete,  album_new_detail, album_update, delete_album_image, get_album, get_album_image, get_albums, upload_base64_image_file, upload_new_image_file

from app.schema.album_schema import AlbumSchema,AlbumResponse,AllalbumResponse,AlbumnewSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db

router = APIRouter(tags=["album"],prefix="/albums")

http_bearer = JWTBearer()

@router.post("/")
async def enter_album_details(album:AlbumnewSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    temp = album_new_detail(db,album)
    return temp

# @router.post("/")
# async def enter_album_details(album:AlbumSchema,keyword: str = Query(default=Required, min_length=3, max_length=3),db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
#     temp = album_detail(db,album,keyword)
#     return temp
    
@router.post("/image/{id}")
async def upload_image_file(album_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    song = upload_new_image_file(db,album_id,uploaded_file) 
    return song

@router.post("/image-base64/{album_id}")
async def upload_b64_img_file(album_id: str,img: str = Body(...) ,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = upload_base64_image_file(db,album_id,img)
    return temp

@router.get("/", response_model=AllalbumResponse)
async def view_all_album_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        temp = get_albums(db)
        if len(temp):
            s = len(temp)
        else:
            s = 1
        return {"records": temp,"totalrecords" : s,"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})


@router.get("/{id}", response_model=AlbumResponse)
async def view_album_details(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_album= get_album(db, album_id)
    if db_album:
        return {"records": db_album,"totalrecords" : 1,"success":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/image/{song_id}")
async def get_image(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = get_album_image(db,album_id)
    return temp


@router.put("/{id}")
async def update_album_details(album_id: int,album: AlbumSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = album_update(db,album_id,album)
    return temp


@router.delete("/{id}")
async def delete_album(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = album_delete(db,album_id)
    return temp


@router.delete("/image/{song_id}")
async def delete_image(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = delete_album_image(db,song_id)
    return user


