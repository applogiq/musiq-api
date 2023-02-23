from fastapi import HTTPException
from config.database import *
from services.user_payment_service import *
from utils.auth_handler import *


def create_user_payment(payment,db,email):
    create_orders=create_payment_service(payment,db,email)
    if create_orders:
        return {"success": True,"message":" created successfully","records":create_orders}
    else:
        raise HTTPException(status_code=404, detail={"message": "Couldn't create order details ...Check your details","success":False})