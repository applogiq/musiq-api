from fastapi import APIRouter,Request, Depends,Body,UploadFile,File,Form,Depends
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

from schemas.podcast_episode_schema import EpisodeSchema,EpisodeOptinalSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.podcast_episode_controller import *

router = APIRouter(tags=["podcast-episode"])

http_bearer = JWTBearer()

  
@router.get("/podcast-episode/{id}")
async def view_episode_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_episode_by_id(db,id)

@router.get("/podcast-episode/list/{podcast_id}")
async def view_episode_podcast_details(podcast_id: int,db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_episode_by_podcastid(db,podcast_id,limit)



#########------- AUDIO STREAMING ---------#########

@router.get("/podcast-audio")
def stream_audio(id: str,request: Request,db: Session = Depends(get_db)):
    episode = episode_get_by_id(db,id)
    if episode:
        return episode_response(db,id,request)
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    
#########------- AUDIO STREAMING ---------#########
