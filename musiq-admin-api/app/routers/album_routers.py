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
    return enter_album_detail(db,album,s["sub"])
    


@router.get("/", response_model=AllalbumResponse)
async def view_all_album_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_album_detail(db,skip,limit)



@router.get("/{id}", response_model=AlbumResponse)
async def view_album_details(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_album_by_id(album_id,db)


@router.put("/{id}")
async def update_album_details(album_id: int,album: AlbumSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_album_details(db,album_id,album,s["sub"])
    


@router.delete("/image/{album_id}")
async def delete_image(album_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_album_image(db,album_id)
    
