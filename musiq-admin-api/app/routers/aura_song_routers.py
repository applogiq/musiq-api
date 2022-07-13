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

###enter new song in aura(current mood) list
@router.post("/")
async def enter_aura_aong_details(auras:AurasongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token) 
    return create_aura_song_details(db,auras,s["sub"])
    
###view all aura's song detail
@router.get("/")
async def view_all_aura_song_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_aura_song_details(db)

##get single aura song detail
@router.get("/{aura_song_id}")
async def view_aura_song_details(aura_song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_aura_details_by_id(db,aura_song_id)
    
###get list of particular aura songs
@router.get("/list/{aura_id}")
async def aura_song_list(aura_id: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_aura_details_by_auraid(db,aura_id)


###to remove song from the particular aura list
@router.delete("/{aura_song_id}")
async def delete_aura_song_details(aura_song_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_aura_song(db,aura_song_id) 
 