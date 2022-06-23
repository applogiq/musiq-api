from fastapi import APIRouter,Depends,Body,HTTPException,Response, status,UploadFile,File
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from controllers.user_controller import *
from schemas.user_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *
from services.user_service import *

router = APIRouter(tags=["users"],prefix='/users')

http_bearer = JWTBearer()

@router.post("/register",status_code=201)
async def create_user(user: UserSchema,response: Response, db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    s = decodeJWT(tokens)
    return register_user(user,db,s["sub"])
    

@router.post("/login")
async def user_login(user: UserLoginSchema,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return login_user(user,db)
    

@router.post("/token-refresh")
def refresh_token(user: Refresh_token,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return token_refresh(user,db)
    

@router.get("/")
async def view_all_users(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,tokens: str = Depends(http_bearer)):
    return get_all_user(db, skip, limit)

@router.get("/{user_id}")
async def get_user_details(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return get_user_by_id(user_id,db)

@router.put('/follow')
def artist_following(user: FollowerSchema,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return follower_details(db,user)
    

@router.put("/{user_id}")
async def update_user_details(user_id: int,user: UserOptional,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    s = decodeJWT(tokens)
    return user_update(user_id,user,db,s["sub"])
    


@router.delete("/image/{user_id}")
async def remove_profile_image(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return delete_profile(user_id,db)
    


##------Forgot Password--------##
    
@router.post("/email")
async def send_otp(email: OtpSend,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return email_otp(db,email)
    

@router.post("/email/otp-verify")
async def otp_verify(email: OtpVerify,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return verify_otp(db,email)
    

@router.put("/email/forget-password")
async def change_password(email: PasswordSchema,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return password_change(db,email)
    

##------Forgot Password--------##



@router.delete("/{user_id}")
async def delete_user(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return user_delete(db,user_id)
    


    
