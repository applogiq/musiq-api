from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session

from app.schema.aura_song_schema import AurasongSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from app.controller.aura_song_controller import aura_song_delete, aura_song_detail, aura_song_fetch, aura_song_update, get_aura_song, get_aura_songs

router = APIRouter(tags=["aura_song"],prefix="/auras/song")

http_bearer = JWTBearer()

@router.post("/")
async def enter_aura_details(auras:AurasongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    aura = aura_song_detail(db,auras)
    return aura

@router.get("/")
async def view_all_aura_song_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    auras = get_aura_songs(db)
    if auras:
        return {"records": auras,"total_records" : len(auras),"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/{aura_id}")
async def view_aura_song_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    auras = get_aura_song(db,aura_id)
    if auras:
        return {"records": auras,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/list/{aura_id}")
async def aura_song_list(aura_id: str,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    auras = aura_song_fetch(db,aura_id)
    if auras:
        return auras
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.put("/{aura_id}")
async def update_aura_details(aura_id: int,auras: AurasongSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = aura_song_update(db,aura_id,auras)
    return temp

@router.delete("/{aura_id}")
async def delete_aura_song_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = aura_song_delete(db,aura_id)
    return temp