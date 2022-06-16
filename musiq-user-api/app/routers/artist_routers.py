from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException,Query
from pydantic import Required
from typing import Union
from sqlalchemy.orm import Session


from schemas.artist_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *
from services.artist_service import *
from controllers.artist_controller import *

router = APIRouter(tags=["artist"],prefix="/artist")

http_bearer = JWTBearer()



@router.get("/")
async def view_all_artist_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    try:
        users = artist_get_all(db,skip,limit)
        return {"success":True,"message":"Details fetched successfully","records": users,"total_records" : len(users)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})


@router.get("/{artist_id}")
async def view_artist_details(artist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    artists = artist_get_by_id(db, artist_id)
    if artists:
        return {"success":True,"message":"Details fetched successfully","records": artists,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/songs/{artist_id}")
async def view_artist_songs(artist_id: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    pass
    # artists = artist_song(db, art_id)
    # if artists:
    #     return {"records": artists,"total_records" : len(artists),"sucess":True}
    # else:
    #     raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

