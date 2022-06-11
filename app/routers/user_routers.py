from fastapi import APIRouter,Depends,Body,HTTPException,Response, status,UploadFile,File
from typing import List
from sqlalchemy.orm import Session


from controllers.user_controller import *
from schemas.user_schema import *
from utils.auth_bearer import JWTBearer
from config.database import get_db

router = APIRouter(tags=["users"],prefix='/users')

http_bearer = JWTBearer()

@router.post("/register",status_code=201)
async def user_register(user: UserSchema,response: Response, db: Session = Depends(get_db)):
    user = register_user(user,db)
    return user

@router.post("/login")
async def user_login(user: UserLoginSchema,db: Session = Depends(get_db)):
    user = login_user(user,db)
    return user

@router.post("/token-refresh")
def refresh_token(user: Refresh_token,db: Session = Depends(get_db)):
    user = token_refresh(user,db)
    return user

# @router.post('/follow')
# def artist_following(user: FollowerSchema,db: Session = Depends(get_db)):
#     user = follower_details(db,user)
#     return user

# @router.post("/profile-picture/{user_id}")
# async def upload_profile_picture(user_id: str,img: str = Body(...) ,db: Session = Depends(get_db)):
#     temp = upload_base64_profile(db,user_id,img)
#     return temp

# @router.get("/profile-picture/{user_id}")
# async def get_profile_image(user_id: int,db: Session = Depends(get_db)):
#     temp = get_profile(db,user_id)
#     return temp

@router.put("/{user_id}")
async def update_user_details(user_id: int,user: UserOptional,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):#,tokens: str = Depends(http_bearer)
    user = user_update(user_id,user,db)
    return user

@router.get("/{user_id}")
async def get_user_details(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):#,tokens: str = Depends(http_bearer)
    user = get_by_id(user_id,db)
    return {"status": True,"message":"fetched Successfully","records":user,"total_records":1}

@router.delete("/image/{user_id}")
async def remove_profile_image(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = delete_profile(user_id,db)
    return user


##------Forgot Password--------##
    
@router.post("/email")
async def send_otp(email: OtpSend,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = email_otp(db,email)
    return user
    # pass

@router.post("/email-otp/verify")
async def otp_verify(email: OtpVerify,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = verify_otp(db,email)
    return user
    # pass

@router.put("/email-otp/")
async def change_password(email: PasswordSchema,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = password_change(db,email)
    return user
