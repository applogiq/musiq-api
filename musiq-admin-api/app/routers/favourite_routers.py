from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
# from controllers.favourite_controller import *

from schemas.favourite_schema import FavouriteSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.favourite_service import *
from controllers.favourite_controller import *

router = APIRouter(tags=["favourites"],prefix='/favourite')

http_bearer = JWTBearer()

@router.post("/")
async def enter_fav_details(fav:FavouriteSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return favourite_detail(db,fav,s["sub"])
    
@router.delete("/")
async def remove_favourites(fav:FavouriteSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_fav_song(db,fav)
    

@router.get("/{user_id}")
async def view_fav_songs(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_fav_details_by_userid(db, user_id)
    

