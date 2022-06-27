from fastapi import APIRouter, Depends,Body,UploadFile,File,Form,Depends
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

from schemas.podcast_schema import PodcastSchema,PodcastOptionalSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.podcast_controller import *

router = APIRouter(tags=["podcast"],prefix='/podcast')

http_bearer = JWTBearer()

@router.post("/")
async def enter_podcast_details(podcast_name : PodcastSchema = Depends() ,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    print(podcast_name.title)
    return create_podcast_details(db,podcast_name,s["sub"],file)
    # return podcast_name,file.filename

@router.get("/")
async def view_all_podcast_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_podcast(db,limit)
  

@router.get("/{id}")
async def view_podcast_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_podcast_by_id(db,id)

@router.put("/{id}")
async def update_podcast_details(id: int,podcast : PodcastOptionalSchema = Depends() ,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    print(podcast.author_id[0].split(","))
    return update_podcast(db,id,podcast,s["sub"],file)
    

@router.delete("/{id}")
async def delete_podcast_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_podcast(db,id)