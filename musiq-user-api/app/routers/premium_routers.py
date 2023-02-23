from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.premium_controller import *

router = APIRouter(tags=["premium"],prefix='/premium')

http_bearer = JWTBearer()


###to get all premium details
@router.get("")
async def view_all_premium_details(db: Session = Depends(get_db),limit: int = 100,token: str = Depends(http_bearer)):
    return get_all_premium(db,limit)
  
###to get particular premium details by it's id
@router.get("/{id}")
async def view_premium_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_premium_by_id(db,id)

