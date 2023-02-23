from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date


###to enter podcase details schema
class PremiumSchema(BaseModel):
    title : str = Field(...)
    price : int = Field(...)
    compare_price : int = None
    validity : int
    
    class Config:
        # orm_mode = True
        schema_extra = {
            "example":{
                "title" : "1 Month",
                "price" :199,
                "compare_price" : 200,
                "validity" : 30 
            }
        }

class PremiumOptionalSchema(BaseModel):
    title : Optional[str] = None
    price :  Optional[int] = None
    compare_price : Optional[int] = None
    validity :  Optional[int] = None
    
    class Config:
        # orm_mode = True
        schema_extra = {
            "example":{
                "title" : "1 Month",
                "price" :199,
                "compare_price" : 200,
                "validity" : 30 
            }
        }