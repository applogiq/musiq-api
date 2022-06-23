from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException,Query
from pydantic import Required
from typing import Union
from sqlalchemy.orm import Session


from schemas.artist_schema import *
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.artist_service import *
from controllers.artist_controller import *

router = APIRouter(tags=["artist"],prefix="/artist")

http_bearer = JWTBearer()

@router.post("/")
async def enter_artist_details(artists:ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token) 
    return create_artist_detail(db,artists,s["sub"])
    

@router.get("/",dependencies=[Depends(http_bearer)])
async def view_all_artist_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_artist_detail(db)


@router.get("/{artist_id}")
async def view_artist_details(artist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_artist_detail_by_id(db,artist_id)


@router.put("/{artist_id}")
async def update_artist_details(artist_id: int,artists:ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token) 
    return  update_artist_details(db,artist_id,artists,s["sub"])
   


@router.delete("/image/{artist_id}")
async def remove_image(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return artist_delete_image(db,art_id)
    
    
