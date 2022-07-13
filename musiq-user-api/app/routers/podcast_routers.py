from fastapi import APIRouter, Depends,Body,UploadFile,File,Form,Depends
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

# from schemas.podcast_schema import PodcastSchema,PodcastOptionalSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.podcast_controller import *

router = APIRouter(tags=["podcast"],prefix='/podcast')

http_bearer = JWTBearer()

###to get all podcast details
@router.get("/")
async def view_all_podcast_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_podcast(db,limit)
  
###to get particular podcast details by it's id
@router.get("/{id}")
async def view_podcast_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_podcast_by_id(db,id)

