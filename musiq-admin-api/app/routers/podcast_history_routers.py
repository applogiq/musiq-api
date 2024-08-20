from fastapi import APIRouter, Depends,Body,UploadFile,File,Form,Depends
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

from schemas.podcast_history_schema import PodcastHistorySchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.podcast_history_controller import *
# from services.sample import *
from services.podcast_history_service import *

router = APIRouter(tags=["podcast-history"],prefix='/podcast-history')

http_bearer = JWTBearer()

###to enter podcast history of particular user
@router.post("/")
async def enter_history_details(history : PodcastHistorySchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    return create_podcast_history(db,history,s["sub"])

# @router.get("/")
# async def view_all_history_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
#     # return get_all_history(db,limit)
#     # return demo_check(db)
#     pass
  
###to get podcast recents of paticular user by their id
@router.get("/{id}")
async def view_history_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_podcast_recent(id)
    # pass
    

# @router.delete("/{id}")
# async def delete_history_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     # return delete_history(db,id)
#     pass