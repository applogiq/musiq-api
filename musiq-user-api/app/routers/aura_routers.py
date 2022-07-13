from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from schemas.aura_schema import AuraSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.aura_service import *
from controllers.aura_controller import *

router = APIRouter(tags=["aura"],prefix="/aura")

http_bearer = JWTBearer()

###get all aura details
@router.get("/")
async def view_all_aura_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_aura_details(db,limit)

###get single aura detail by it's id     
@router.get("/{aura_id}")
async def view_aura_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_aura_details_by_id(db, aura_id)
    