from fastapi import APIRouter,Depends,Body,HTTPException,Response, status,UploadFile,File

from app.schema.user_schema import FollowerSchema, UserSchema,UserLoginSchema,Refresh_token,UserOptional
from app.controller.user_controller import delete_profile, follower_details, get_profile, get_user,token_refresh,get_db,get_users,register_user,login_user, upload_base64_profile, upload_new_profile, user_delete, user_update
from app.auth.auth_bearer import JWTBearer
from sqlalchemy.orm import Session


router = APIRouter()

http_bearer = JWTBearer()

@router.post("/users/register", tags=["users"])
async def user_register(user: UserSchema,response: Response, db: Session = Depends(get_db)):
    user = register_user(db,user,response)
    return user

@router.post("/users/login",  tags=["users"])
async def user_login(user: UserLoginSchema = Body(...),db: Session = Depends(get_db)):
    user = login_user(db,user)
    return user

@router.post('/users/refresh', tags=["users"])
def refresh_token(user: Refresh_token = Body(...),db: Session = Depends(get_db)):
    user = token_refresh(db,user)
    return user

@router.post('/users/follow', tags=["users"])
def artist_following(user: FollowerSchema,db: Session = Depends(get_db)):
    user = follower_details(db,user)
    return user

@router.post("/users/profile-base64/{user_id}",tags=["users"])
async def upload_b64_profile(user_id: str,img: str = Body(...) ,db: Session = Depends(get_db)):
    temp = upload_base64_profile(db,user_id,img)
    return temp

@router.post("/users/profile/{user_id}",tags=["users"])
async def upload_profile(user_id: str,uploaded_file: UploadFile = File(...),db: Session = Depends(get_db)):#,token: str = Depends(http_bearer)
    song = upload_new_profile(db,user_id,uploaded_file)
    return song

@router.get("/users",tags=["users"])
def view_all_users(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,token: str = Depends(http_bearer)):
    try:
        users = get_users(db, skip=skip, limit=limit)
        return {"records": users,"total_records" : len(users),"success":True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

@router.get("/users/{user_id}",tags=["users"])
async def view_single_user(user_id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    db_user = get_user(db, user_id)
    if db_user:
        return {"records": db_user,"total_records" : 1,"sucess":True}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

@router.get("/users/profile/{user_id}",tags=["users"])
async def get_profile_image(user_id: int,db: Session = Depends(get_db)):
    temp = get_profile(db,user_id)
    return temp

@router.put("/users/{user_id}",tags=["users"])
async def update_user_details(user_id: int,user: UserOptional,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = user_update(db,user_id,user)
    return user

@router.delete("/users/{user_id}",tags=["users"])
async def delete_user(user_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    user = user_delete(db,user_id)
    return user

       
@router.delete("/users/profile/{user_id}",tags=["users"])
async def remove_profile(user_id: int,db: Session = Depends(get_db)):
    user = delete_profile(db,user_id)
    return user


