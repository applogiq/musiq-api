from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
# from app.controller.genre_controller import genre_delete, genre_detail, genre_update, get_genre, get_genres

from schemas.genre_schema import GenreSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from services.genre_service import *
from utils.auth_handler import decodeJWT
from controllers.genre_controller import *


router = APIRouter(tags=["genres"],prefix='/genres')

http_bearer = JWTBearer()

@router.post("/")
async def enter_genre_details(genre:GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    return genre_detail(db,genre,s["sub"])
    
@router.get("/")
async def view_all_genre_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_genre_details(db)

@router.get("/{id}")
async def view_genre_details(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_genre_by_id(db,genre_id)

@router.put("/{id}")
async def update_genre_details(genre_id: int,genre: GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_genre_details(db,genre_id,genre,s["sub"])


@router.delete("/{id}")
async def delete_genre(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_genre_details(db,genre_id)
    
