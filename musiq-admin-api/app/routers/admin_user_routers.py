from fastapi import APIRouter,Depends,Body,HTTPException,Response, status,UploadFile,File
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from controllers.user_controller import *
from controllers.admin_user_controller import *
from schemas.user_schema import *
from schemas.admin_user_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *

router = APIRouter(tags=["admin users"],prefix='/admin-users')

http_bearer = JWTBearer()

@router.post("/register",status_code=201)
async def user_register(user: AdminSchema,response: Response, db: Session = Depends(get_db)):
    user = register_admin(user,db)
    return user

@router.post("/login")
async def user_login(user: UserLoginSchema,db: Session = Depends(get_db)):
    user = login_admin(user,db)
    return user


@router.post("/token-refresh")
def refresh_token(user: Refresh_token,db: Session = Depends(get_db)):
    user = admin_token_refresh(user,db)
    return user

@router.get("/")
async def view_all_users(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,tokens: str = Depends(http_bearer)):
    try:
        users = admin_get_all(db, skip=skip, limit=limit)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"totalrecords":s,"success": True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/{user_id}")
async def get_user_details(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):#,tokens: str = Depends(http_bearer)
    user = admin_get_by_id(user_id,db)
    if user:
        return {"status": True,"message":"fetched Successfully","records":user,"total_records":1}
    else:
        raise HTTPException(status_code=422, detail={"message": "Couldn't fetch...Check your id","success":False})

@router.put("/{user_id}")
async def update_user_details(user_id: int,user: AdminOptional,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):#,tokens: str = Depends(http_bearer)
    user = admin_user_update(user_id,user,db)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = admin_delete(db,user_id)
    return user
    

