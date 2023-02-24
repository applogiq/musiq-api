from pydantic import BaseModel,Field
from typing import Optional


class UserPaymentSchema(BaseModel):
    """Schema for swagger documentaion for Create order details"""

    user_id:int=Field(...)
    payment_price:Optional[int]=None
    premier_status:str=Field(...)
    class Config:
         schema_extra = {
                "example":{ 
                    "user_id":1,
                    "payment_price":300,
                    "premier_status":"1 month"
                }}


class CallBackSchema(BaseModel):
    """Schema for swagger documentaion for Get Payment verify details"""

    user_id:int=Field(...)
    premier_status:str=Field(...)
    validity:int=Field(...)
    razorpay_order_id:str=Field(...)
    razorpay_payment_id:str=Field(...)
    razorpay_signature:str=Field(...)
    class Config:
        schema_extra = {
            "example":{
                "user_id":1,
                "premier_status":"1 month",
                "validity":30,
                "razorpay_order_id":"order_L6m3cToeH9FHW7",                        
                "razorpay_payment_id":"payment_L6m3cToeH9FHW7",
                "razorpay_signature":"sign_L6m3cToeH9FHW7"                    
            }
        }