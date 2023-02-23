from pydantic import BaseModel,Field
from typing import Optional


class UserPaymentSchema(BaseModel):
    """Schema for swagger documentaion for Create order details"""

    user_id:int=Field(...)
    payment_price:int=Field(...)
    premier_status:str=Field(...)
    class Config:
         schema_extra = {
                "example":{ 
                    "user_id":1,
                    "payment_price":300,
                    "premier_status":"1 month"
                }}
