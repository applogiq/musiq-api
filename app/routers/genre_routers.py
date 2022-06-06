from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.controller.genre_controller import genre_delete, genre_detail, genre_update, get_genre, get_genres

from app.schema.genre_schema import GenreSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db


router = APIRouter(tags=["genres"],prefix='/genres')

http_bearer = JWTBearer()

@router.post("/")
async def enter_genre_details(genre:GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    temp = genre_detail(db,genre)
    return temp

@router.get("/")
async def view_all_genre_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        temp = get_genres(db)
        return {"records": temp,"total_records" : len(temp),"success":True}
    except:
        # return {"message": "couldn't fetch","success":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})


@router.get("/{id}")
async def view_genre_details(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        return {"records": db_genre,"total_records" : 1,"sucess":True}
    else:
        # return {"message": "couldn't fetch,check your id","sucess":False}
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


@router.put("/{id}")
async def update_genre_details(genre_id: int,genre: GenreSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = genre_update(db,genre_id,genre)
    return temp


@router.delete("/{id}")
async def delete_genre(genre_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = genre_delete(db,genre_id)
    return temp