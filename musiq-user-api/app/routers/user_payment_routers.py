from fastapi import APIRouter,Depends,Body,HTTPException,Response, status,UploadFile,File
from typing import List
from sqlalchemy.orm import Session

from controllers.user_payment_controller import *
from schemas.user_payment_schema import *
from utils.auth_bearer import JWTBearer
from config.database import *


router = APIRouter(tags=["userpayment"],prefix='/users-payment')


http_bearer = JWTBearer()


@router.post("/create",status_code=201)
async def create_payment(payment:UserPaymentSchema,response:Response,db:Session = Depends(get_db),tokens:str = Depends(http_bearer)):
    s = decodeJWT(tokens)
    return create_user_payment(payment,db,s["sub"])