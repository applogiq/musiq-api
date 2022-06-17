from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
# from app.controller.genre_controller import genre_delete, genre_detail, genre_update, get_genre, get_genres

from schemas.genre_schema import GenreSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from services.genre_service import *
from utils.auth_handler import decodeJWT
# from app.controller.user_controller import get_db


router = APIRouter(tags=["genres"],prefix='/genres')

http_bearer = JWTBearer()

@router.post("/")
async def enter_genre_details(genre:GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    temp = genre_detail(db,genre,s["sub"])
    if temp:
        return {"success":True,'message': "song details added","records": temp}
    else:
        return {'message': "Check your details","success": False}
  

@router.get("/")
async def view_all_genre_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        temp = genre_get_all(db)
        return {"success":True,"message": {"genre details fetched successfully"},"records": temp,"total_records" : len(temp)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})



@router.get("/{id}")
async def view_genre_details(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_genre = genre_get_by_id(db, genre_id)
    if db_genre:
        return {"success":True,"message":"Fetched successfully","records": db_genre,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})



@router.put("/{id}")
async def update_genre_details(genre_id: int,genre: GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    temp = genre_update(db,genre_id,genre,s["sub"])
    return temp
    # pass


@router.delete("/{id}")
async def delete_genre(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = genre_delete(db,genre_id)
    return temp
