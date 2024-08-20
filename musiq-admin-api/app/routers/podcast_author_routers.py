from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.podcast_author_schema import PodcastAuthorSchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.podcast_author_controller import *


router = APIRouter(tags=["author"],prefix='/podcast-author')

http_bearer = JWTBearer()

###to enter podcast's author details
@router.post("/")
async def enter_author_details(author: PodcastAuthorSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    return create_author_details(db,author,s["sub"])
    # return author
    
###get all author's details
@router.get("/")
async def view_all_author_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_author(db,limit)
  
###get single author details by their id
@router.get("/{id}")
async def view_author_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_author_by_id(db,id)
    
###to update existing author details
@router.put("/{id}")
async def update_author_details(id: int,author:PodcastAuthorSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_author(db,id,author,s["sub"])
    
###to delete particular author details by their id
@router.delete("/{id}")
async def delete_author_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_author(db,id)
    

