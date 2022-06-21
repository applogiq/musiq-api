from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session


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
async def remove_favourites(fav:FavouriteSchema,db: Session = Depends(get_db)):
    user = fav_delete(db,fav)
    return user

@router.get("/{user_id}")
async def view_fav_songs(user_id: int,db: Session = Depends(get_db)):
    users = fav_get_by_userid(db, user_id)
    if users:
        return {"success":True,"message":"successfully fetched","records": users,"total_records" : len(users)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})
    

