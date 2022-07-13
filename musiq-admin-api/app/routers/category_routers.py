from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.category_schema import CategorySchema
from utils.auth_bearer import JWTBearer
from config.database import *
from utils.auth_handler import decodeJWT
from controllers.category_controller import *


router = APIRouter(tags=["categories"],prefix='/category')

http_bearer = JWTBearer()

###create new category for podcast
@router.post("/")
async def enter_category_details(category:CategorySchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)): #
    s = decodeJWT(token)
    return create_category_details(db,category,s["sub"])
    

###get all category details 
@router.get("/")
async def view_all_category_details(db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_all_category_details(db)
    
###get particular category detail by it's id
@router.get("/{id}")
async def view_category_details(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return get_category_by_id(db,id)
    

###to update exixiting category detail
@router.put("/{id}")
async def update_category_details(id: int,category: CategorySchema,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    s = decodeJWT(token)
    return update_category(db,id,category,s["sub"])
    

###to delete category detail by it's id
@router.delete("/{id}")
async def delete_category(id: int,db: Session = Depends(get_db),token: str = Depends(http_bearer)):
    return delete_category_details(db,id)
    
    