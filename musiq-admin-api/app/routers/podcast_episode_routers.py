from fastapi import APIRouter, Depends,Body,UploadFile,File,Form,Depends
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

router = APIRouter(tags=["podcast-episode"],prefix='/podcast-episode')

http_bearer = JWTBearer()

@router.post("/")
async def enter_podcast_episode_details(episode :EpisodeSchema = Depends() ,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    return create_episode_details(db,episode,s["sub"],file)
    # return episode_name,file.filename

@router.get("/")
async def view_all_episode_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_episode(db,limit)
  

@router.get("/{id}")
async def view_episode_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_episode_by_id(db,id)

@router.get("/list/{podcast_id}")
async def view_episode_podcast_details(podcast_id: int,db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_episode_by_podcastid(db,podcast_id,limit)

# @router.put("/{id}")
# async def update_episode_details(id: int,episode : EpisodeOptinalSchema = Depends() ,file: Optional[UploadFile] = File(None),db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     s = decodeJWT(token)
#     print(episode.author_id[0].split(","))
#     return update_episode(db,id,episode,s["sub"],file)
    

# @router.delete("/{id}")
# async def delete_episode_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
#     return delete_episode(db,id)