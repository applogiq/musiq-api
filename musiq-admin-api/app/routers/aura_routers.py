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

@router.post("/")
async def enter_aura_details(auras:AuraSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    s = decodeJWT(token)
    return create_aura_details(db,auras,s["sub"])

@router.get("/")
async def view_all_aura_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_aura_details(db)
    
@router.get("/{aura_id}")
async def view_aura_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_aura_details_by_id(db, aura_id)
    
@router.put("/{aura_id}")
async def update_aura_details(aura_id: int,auras: AuraSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_aura_details(db,aura_id,auras,s["sub"])
    
   
@router.delete("/{aura_id}")
async def delete_aura_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_aura_details(db,aura_id)
    

@router.delete("/image/{aura_id}")
async def remove_aura_image(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_aura_image(db,aura_id)
    
