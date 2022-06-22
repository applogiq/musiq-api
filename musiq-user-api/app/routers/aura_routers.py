from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from schemas.aura_schema import AuraSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.aura_service import *


router = APIRouter(tags=["aura"],prefix="/aura")

http_bearer = JWTBearer()

@router.get("/")
async def view_all_aura_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # pass
    try:
        users = aura_get_all(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    
@router.get("/{aura_id}")
async def view_aura_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    # pass
    auras = aura_get_by_id(db, aura_id)
    if auras:
        return {"records": auras,"total_records" : 1,"success":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})