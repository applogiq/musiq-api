from fastapi import APIRouter, Depends,UploadFile,File,Request,Body,Query,HTTPException
from pydantic import Required
from typing import Union,List
from sqlalchemy.orm import Session


from utils.auth_handler import *
from schemas.album_schema import AlbumSchema,AlbumResponse,AllalbumResponse
from utils.auth_bearer import JWTBearer
from config.database import *
from controllers.album_controller import *

router = APIRouter(tags=["album"],prefix="/albums")

http_bearer = JWTBearer()

@router.post("/")
async def enter_album_details(album:AlbumSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    temp = album_detail(db,album,s["sub"])
    return temp



@router.get("/", response_model=AllalbumResponse)
async def view_all_album_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    try:
        temp = album_get_all(db,skip,limit)
        if len(temp):
            s = len(temp)
        else:
            s = 1
        return {"success":True,"message": "Fetched Successfully","records": temp,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})



@router.get("/{id}", response_model=AlbumResponse)
async def view_album_details(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_album= album_get_by_id(album_id,db)
    if db_album:
        return {"success":True,"message": "Fetched Successfully","records": db_album,"totalrecords" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


@router.put("/{id}")
async def update_album_details(album_id: int,album: AlbumSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    temp = album_update(db,album_id,album,s["sub"])
    return temp


@router.delete("/image/{song_id}")
async def delete_image(song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = delete_album_image(db,song_id)
    return user
