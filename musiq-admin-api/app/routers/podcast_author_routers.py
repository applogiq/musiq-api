# from email.mime import image, multipart
from fastapi import APIRouter, Depends,Body,UploadFile,File
import os
from typing import Optional,Union,List
from sqlalchemy.orm import Session
from fastapi.responses import Response
from pydantic import Field

from schemas.podcast_author_schema import PodcastAuthorSchema
from utils.auth_bearer import JWTBearer
from config.database import *
# from services.genre_service import *
from utils.auth_handler import decodeJWT
from controllers.podcast_author_controller import *


router = APIRouter(tags=["author"],prefix='/podcast-author')
# router = FastAPI()

http_bearer = JWTBearer()

# @router.post("/")
# async def enter_author_details(uploaded_file: UploadFile,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
#     # s = decodeJWT(token)
#     # return create_author_details(db,author,s["sub"])
#     pass

# @router.post("/image/{art_id}")
# async def upload_img_file(art_id: str,uploaded_file: UploadFile,db: Session = Depends(get_db)): 
#     # artist = upload_art_image_file(db,art_id,uploaded_file)
#     # return artist
    # pass
    
@router.get("/")
async def view_all_author_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # return get_all_author_details(db)
    pass

@router.get("/{id}")
async def view_author_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # return get_author_by_id(db,id)
    pass

@router.put("/{id}")
async def update_author_details(id: int,author: PodcastAuthorSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # s = decodeJWT(token)
    # return update_author(db,id,author,s["sub"])
    pass

@router.post("/")
def new(file: UploadFile = File(...)):
    return {"filename": file.filename}

@router.get("/vbvbvbj")
async def create_upload_file(file: str,db: Session = Depends(get_db)):
    return {"filename": file.filename}