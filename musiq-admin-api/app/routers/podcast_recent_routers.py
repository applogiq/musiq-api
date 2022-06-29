from fastapi import APIRouter, Depends,Body,UploadFile,File,Form,Depends
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

from schemas.podcast_recent_schema import PodcastRecentSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
# from controllers.podcast_controller import *
from services.sample import *

router = APIRouter(tags=["podcast-recent"],prefix='/podcast-recent')

http_bearer = JWTBearer()

@router.post("/")
async def enter_recent_details(recent : PodcastRecentSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    # s = decodeJWT(token)
    # print(recent.title)
    # return demo_check(db)
    # # return podcast_name,file.filename
    pass

@router.get("/")
async def view_all_recent_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    # return get_all_recent(db,limit)
    return demo_check(db)
    # pass
  

@router.get("/{id}")
async def view_recent_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # return get_recent_by_id(db,id)
    pass
    

@router.delete("/{id}")
async def delete_recent_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # return delete_recent(db,id)
    pass