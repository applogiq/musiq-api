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



@router.get("/",dependencies=[Depends(http_bearer)])
async def view_all_artist_details(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_artist_detail(db,skip,limit)


@router.get("/{artist_id}")
async def view_artist_details(artist_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_artist_detail_by_id(db,artist_id)



