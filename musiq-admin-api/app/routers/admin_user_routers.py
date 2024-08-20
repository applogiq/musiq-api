from fastapi import APIRouter,Depends,Response
from sqlalchemy.orm import Session


from controllers.user_controller import *
from controllers.admin_user_controller import *
from schemas.user_schema import *
from schemas.admin_user_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *

router = APIRouter(tags=["admin users"],prefix='/admin-users')

http_bearer = JWTBearer()

###to register as admin
@router.post("/register",status_code=201)
async def user_register(user: AdminSchema,response: Response, db: Session = Depends(get_db)):
    return register_admin(user,db)
    
###to login as admin
@router.post("/login")
async def user_login(user: UserLoginSchema,db: Session = Depends(get_db)):
    return login_admin(user,db)
    
###to refresh the access token
@router.post("/token-refresh")
def refresh_token(user: Refresh_token,db: Session = Depends(get_db)):
    return admin_token_refresh(user,db)

###to get all admin details
@router.get("/")
async def view_all_users(db: Session = Depends(get_db),skip: int = 0, limit: int = 100,tokens: str = Depends(http_bearer)):
    return get_all_admin_details(db, skip, limit)

###to get single admin user detail
@router.get("/{admin_id}")
async def get_admin_details(admin_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):#,tokens: str = Depends(http_bearer)
    return get_admin_by_id(admin_id,db)

###to update details for existing admin
@router.put("/{admin_id}")
async def update_admin_details(admin_id: int,admin: AdminOptional,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):#,tokens: str = Depends(http_bearer)
    s = decodeJWT(tokens) 
    return  update_admin(admin_id,admin,db,s["sub"])
    
###to delete admin user details
@router.delete("/{admin_id}")
async def delete_admin(admin_id: int,db: Session = Depends(get_db),tokens: str = Depends(http_bearer)):
    return delete_admin_details(db,admin_id)
    

