from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session
from app.controller.favourite_controller import fav_delete, fav_song_detail, get_favourite, get_favourite_songs, get_favourites

from app.schema.favourite_schema import FavouriteSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db

router = APIRouter()

http_bearer = JWTBearer()

@router.post("/favourite", tags=["favourites"])
async def enter_fav_details(fav:FavouriteSchema,db: Session = Depends(get_db)): #,token: str = Depends(http_bearer)
    temp = fav_song_detail(db,fav)
    return temp
# fav_delete

@router.delete("/favourite", tags=["favourites"])
async def remove_favourites(fav:FavouriteSchema,db: Session = Depends(get_db)):
    user = fav_delete(db,fav)
    return user

@router.get("/favourite", tags=["favourites"])
async def view_all_fav_details(db: Session = Depends(get_db)):
    try:
        users = get_favourites(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/favourite/{fav_id}", tags=["favourites"])
async def view_artist_details(fav_id: int,db: Session = Depends(get_db)):
    users = get_favourite(db, fav_id)
    if users:
        return {"records": users,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/favourite/user/{user_id}", tags=["favourites"])
async def view_fav_songs(user_id: int,db: Session = Depends(get_db)):
    users = get_favourite_songs(db, user_id)
    if users:
        return {"records": users,"total_records" : len(users),"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

