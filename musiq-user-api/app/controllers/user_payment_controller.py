from fastapi import HTTPException
from config.database import *
from services.user_payment_service import *
from utils.auth_handler import *


def create_user_payment(payment,db,email):
    create_orders=create_payment_service(payment,db,email)
    if create_orders:
        return {"success": True,"message":"Created successfully","records":create_orders}
    else:
        raise HTTPException(status_code=400, detail={"message": "Check your details","success":False})
    

def callback_controller(payment,db,email):
    create_orders=callback_service(payment,db,email)
    if create_orders:
        return {"success": True,"message":"Updated successfully","records":create_orders}
    else:
        raise HTTPException(status_code=400, detail={"message": "Check your details","success":False})