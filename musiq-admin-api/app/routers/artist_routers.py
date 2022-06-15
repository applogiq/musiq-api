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
    print(s["sub"])
    artist = artist_detail(db,artists,s["sub"])
    return artist


@router.get("/",dependencies=[Depends(http_bearer)])
async def view_all_artist_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    try:
        users = artist_get_all(db,skip,limit)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})


@router.get("/{artist_id}")
async def view_artist_details(artist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # pass
    artists = artist_get_by_id(db, artist_id)
    if artists:
        return {"records": artists,"total_records" : 1,"sucess":True}
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

@router.put("/{artist_id}")
async def update_artist_details(artist_id: int,artists:ArtistSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = artist_update(db,artist_id,artists)
    return temp


@router.delete("/image/{artist_id}")
async def remove_image(art_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = artist_delete_image(db,art_id)
    return user
    # pass