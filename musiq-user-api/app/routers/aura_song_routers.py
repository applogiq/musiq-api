from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from schemas.aura_song_schema import AurasongSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.aura_song_service import *
from controllers.aura_song_controller import *

router = APIRouter(tags=["aura song"],prefix="/aura-song")

http_bearer = JWTBearer()



@router.get("/")
async def view_all_aura_song_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_aura_song_details(db,limit)



@router.get("/list/{aura_id}")
async def aura_song_list(aura_id: str,db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_aura_details_by_auraid(db,aura_id,limit)

