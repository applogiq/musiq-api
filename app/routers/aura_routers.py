from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session


from app.schema.aura_schema import AuraSchema,AuranewSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from app.controller.aura_controllers import aura_delete, aura_detail, aura_new_detail, aura_update, delete_aura_image, get_aura, get_aura_image, get_auras, upload_aura_image_file, upload_base64_aura_file

router = APIRouter(tags=["aura"],prefix="/aura")

http_bearer = JWTBearer()

@router.post("/new")
async def enter_aura_details(auras:AuranewSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    aura = aura_new_detail(db,auras)
    return aura

@router.post("/")
async def enter_aura_details(auras:AuraSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    aura = aura_detail(db,auras)
    return aura
    

@router.post("/image/{aura_id}")
async def upload_img_file(aura_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db),token: str = Depends(http_bearer)): 
    aura = upload_aura_image_file(db,aura_id,uploaded_file)
    return aura
    

@router.post("/image-base64/{aura_id}")
async def upload_b64_img_file(aura_id: str,img: str = Body(...) ,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = upload_base64_aura_file(db,aura_id,img)
    return temp
    

@router.get("/")
async def view_all_aura_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    try:
        users = get_auras(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    

@router.get("/{aura_id}")
async def view_aura_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    auras = get_aura(db, aura_id)
    if auras:
        return {"records": auras,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
    
@router.get("/image/{aura_id}")
async def aura_image(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = get_aura_image(db,aura_id)
    return temp

    
@router.put("/{aura_id}")
async def update_aura_details(aura_id: int,auras: AuranewSchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = aura_update(db,aura_id,auras)
    return temp
   

@router.delete("/{aura_id}")
async def delete_aura_details(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = aura_delete(db,aura_id)
    return temp


@router.delete("/image/{aura_id}")
async def remove_aura_image(aura_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    temp = delete_aura_image(db,aura_id)
    return temp
