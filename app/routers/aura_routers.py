from fastapi import APIRouter, Body, Depends,UploadFile,File,HTTPException
from sqlalchemy.orm import Session


from app.schema.aura_schema import AuraSchema
from app.auth.auth_bearer import JWTBearer
from app.controller.user_controller import get_db
from app.controller.aura_controllers import aura_delete, aura_detail, aura_update, get_aura, get_aura_image, get_auras, upload_aura_image_file, upload_base64_aura_file

router = APIRouter()

http_bearer = JWTBearer()

@router.post("/aura", tags=["aura"])
async def enter_aura_details(auras:AuraSchema,db: Session = Depends(get_db)): #,token: str = Depends(http_bearer)
    aura = aura_detail(db,auras)
    return aura
    

@router.post("/aura/image/{aura_id}",tags=["aura"])
async def upload_img_file(aura_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db)): #
    aura = upload_aura_image_file(db,aura_id,uploaded_file)
    return aura
    

@router.post("/aura/image-base64/{aura_id}",tags=["aura"])
async def upload_b64_img_file(aura_id: str,img: str = Body(...) ,db: Session = Depends(get_db)):
    temp = upload_base64_aura_file(db,aura_id,img)
    return temp
    

@router.get("/aura", tags=["aura"])
async def view_all_aura_details(db: Session = Depends(get_db)):
    try:
        users = get_auras(db)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})
    

@router.get("/aura/{aura_id}", tags=["aura"])
async def view_aura_details(aura_id: int,db: Session = Depends(get_db)):
    auras = get_aura(db, aura_id)
    if auras:
        return {"records": auras,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
    
@router.get("/aura/image/{aura_id}", tags=["aura"])
async def aura_image(aura_id: int,db: Session = Depends(get_db)):
    temp = get_aura_image(db,aura_id)
    return temp
    # pass

# @router.get("/aura/songs/{art_id}", tags=["aura"])
# async def view_aura_songs(art_id: str,db: Session = Depends(get_db)):#
#     auras = aura_song(db, art_id)
#     if auras:
#         # return auras
#         return {"records": auras,"total_records" : len(auras),"sucess":True}
#     else:
#         # return {"message": "couldn't fetch,check your id","sucess":False}
#         raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
    
@router.put("/aura/{aura_id}", tags=["aura"])
async def update_aura_details(aura_id: int,auras: AuraSchema,db: Session = Depends(get_db)):
    temp = aura_update(db,aura_id,auras)
    return temp
   

@router.delete("/aura/{aura_id}", tags=["aura"])
async def delete_aura_details(aura_id: int,db: Session = Depends(get_db)):
    temp = aura_delete(db,aura_id)
    return temp
    # pass

