from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from schemas.aura_song_schema import AurasongSchema
from utils.auth_bearer import JWTBearer
from utils.auth_handler import *
from config.database import *
from services.aura_song_service import *

router = APIRouter(tags=["aura song"],prefix="/aura-song")

http_bearer = JWTBearer()



@router.get("/")####limit
async def view_all_aura_song_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    auras = aura_song_get_all(db)
    if auras:
        return {"records": auras,"total_records" : len(auras),"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})



@router.get("/list/{aura_id}")
async def aura_song_list(aura_id: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    auras = aura_song_get_by_auraid(db,aura_id)
    if auras:
        return auras
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

