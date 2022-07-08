# from email.mime import image, multipart
from fastapi import APIRouter, Depends,Body,UploadFile,File,Form
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field
# from app.schemas.podcast_schema import PodcastSchema

from schemas.podcast_author_schema import PodcastAuthorSchema
from schemas.song_schema import SongSchema
from utils.auth_bearer import JWTBearer
from config.database import *
# from services.genre_service import *
from utils.auth_handler import decodeJWT
from controllers.podcast_author_controller import *


router = APIRouter(tags=["author"],prefix='/podcast-author')
# router = FastAPI()

http_bearer = JWTBearer()

@router.post("/")
async def enter_author_details(author: PodcastAuthorSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    return create_author_details(db,author,s["sub"])
    # return author
    

@router.get("/")
async def view_all_author_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_author(db,limit)
  

@router.get("/{id}")
async def view_author_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_author_by_id(db,id)
    

@router.put("/{id}")
async def update_author_details(id: int,author:PodcastAuthorSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_author(db,id,author,s["sub"])
    

@router.delete("/{id}")
async def delete_author_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_author(db,id)
    

