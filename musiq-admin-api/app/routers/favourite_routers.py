from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
# from app.controller.favourite_controller import fav_delete, fav_song_detail, get_favourite, get_favourite_songs, get_favourites

from schemas.favourite_schema import FavouriteSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.favourite_service import *

router = APIRouter(tags=["favourites"],prefix='/favourite')

http_bearer = JWTBearer()

@router.post("/")
async def enter_fav_details(fav:FavouriteSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    temp = fav_song_detail(db,fav,s["sub"])
    return temp

@router.delete("/")
async def remove_favourites(fav:FavouriteSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    user = fav_delete(db,fav)
    return user

@router.get("/")
async def view_all_fav_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        users = fav_get_all(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

# @router.get("/{fav_id}")
# async def view_artist_details(fav_id: int,db: Session = Depends(get_db)):
#     pass
#     # users = get_favourite(db, fav_id)
    # if users:
    #     return {"records": users,"total_records" : 1,"sucess":True}
    # else:
    #     raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/{user_id}")
async def view_fav_songs(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    users = fav_get_by_userid(db, user_id)
    if users:
        return {"success":True,"message":"successfully fetched","records": users,"total_records" : len(users)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})
    

