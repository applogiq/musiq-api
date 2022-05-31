from fastapi import APIRouter, Depends,UploadFile,File,Request,Body,Query,HTTPException
from pydantic import Required
from typing import Union
from sqlalchemy.orm import Session
from app.controller.album_controller import album_delete, album_detail, album_update, delete_album_image, get_album, get_album_image, get_albums, upload_base64_image_file, upload_new_image_file


from app.schema.album_schema import AlbumSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db


router = APIRouter()

http_bearer = JWTBearer()

@router.post("/albums", tags=["album"])
async def enter_album_details(album:AlbumSchema,keyword: str = Query(default=Required, min_length=3, max_length=3),db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    temp = album_detail(db,album,keyword)
    return temp
    

@router.get("/albums", tags=["album"])
async def view_all_album_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        temp = get_albums(db)
        return {"records": temp,"total_records" : len(temp),"success":True}
    except:
        # return {"message": "couldn't fetch","success":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})


@router.get("/albums/{id}", tags=["album"])
async def view_album_details(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_album= get_album(db, album_id)
    if db_album:
        return {"records": db_album,"total_records" : 1,"sucess":True}
    else:
        # return {"message": "couldn't fetch,check your id","sucess":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.post("/albums/image/{id}",tags=["album"])
async def upload_image_file(album_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    song = upload_new_image_file(db,album_id,uploaded_file) 
    return song


@router.put("/albums/{id}", tags=["album"])
async def update_album_details(album_id: int,album: AlbumSchema,keyword: Union[str, None] = Query(default=None, fixed_length=3),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = album_update(db,album_id,album,keyword)
    return temp


@router.delete("/albums/{id}", tags=["album"])
async def delete_album(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = album_delete(db,album_id)
    return temp


@router.post("/albums/image-base64/{album_id}",tags=["album"])
async def upload_b64_img_file(album_id: str,img: str = Body(...) ,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = upload_base64_image_file(db,album_id,img)
    return temp


@router.get("/albums/image/{song_id}", tags=["album"])
async def get_image(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = get_album_image(db,album_id)
    return temp

@router.delete("/albums/image/{song_id}", tags=["album"])
async def delete_image(song_id: int,db: Session = Depends(get_db)):
    user = delete_album_image(db,song_id)
    return user