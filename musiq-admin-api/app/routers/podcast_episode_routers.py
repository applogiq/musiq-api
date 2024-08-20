from fastapi import APIRouter,Request, Depends,Body,UploadFile,File,Form,Depends
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

from schemas.podcast_episode_schema import EpisodeSchema,EpisodeOptionalSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.podcast_episode_controller import *

router = APIRouter(tags=["podcast-episode"])

http_bearer = JWTBearer()

###to enter episode details for particular details
@router.post("/podcast-episode")
async def enter_podcast_episode_details(episode :EpisodeSchema = Depends() ,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    return create_episode_details(db,episode,s["sub"],file)
    # return episode_name,file.filename

###to view all podcast's episode details
@router.get("/podcast-episode")
async def view_all_episode_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_episode(db,limit)
  
###to get single episode details
@router.get("/podcast-episode/{id}")
async def view_episode_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_episode_by_id(db,id)

###to get particular podcast's episodes details
@router.get("/podcast-episode/list/{podcast_id}")
async def view_episode_podcast_details(podcast_id: int,db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_episode_by_podcastid(db,podcast_id,limit)

###to update exixting episode details
@router.put("/podcast-episode/{id}")
async def update_episode_details(id: int,episode : EpisodeOptionalSchema = Depends() ,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_episode(db,id,episode,s["sub"],file)

###to delete podcast episode details by it's id   
@router.delete("/podcast-episode/{id}")
async def delete_episode_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_episode(db,id)

#########------- AUDIO STREAMING ---------#########

@router.get("/podcast-audio")
def stream_audio(id: str,request: Request,db: Session = Depends(get_db)):
    episode = episode_get_by_id(db,id)
    if episode:
        return episode_response(db,id,request)
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False}) 
    
#########------- AUDIO STREAMING ---------#########
