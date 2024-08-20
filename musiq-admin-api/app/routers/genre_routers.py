from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.genre_schema import GenreSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from services.genre_service import *
from utils.auth_handler import decodeJWT
from controllers.genre_controller import *


router = APIRouter(tags=["genres"],prefix='/genres')

http_bearer = JWTBearer()

###to enter new genre details
@router.post("/")
async def enter_genre_details(genre:GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    return create_genre_details(db,genre,s["sub"])

###to get all genre details  
@router.get("/")
async def view_all_genre_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_genre_details(db)

##to get particular gentre detail by their id
@router.get("/{genre_id}")
async def view_genre_details(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_genre_by_id(db,genre_id)

###to update existing genre details
@router.put("/{genre_id}")
async def update_genre_details(genre_id: int,genre: GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_genre(db,genre_id,genre,s["sub"])

###to delete particular genre detail bu their id
@router.delete("/{genre_id}")
async def delete_genre(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_genre_details(db,genre_id)
    
