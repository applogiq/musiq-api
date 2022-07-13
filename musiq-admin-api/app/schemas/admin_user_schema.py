from pydantic import BaseModel,Field
from typing import Dict,Optional,List

###to enter admin user details schema
class AdminSchema(BaseModel):
    name : str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "name" : "Name",
                "email": "abcdef@x.com",
                "password": "Password@67"
                
            }
        }

###to update admin user details schema
class AdminOptional(BaseModel):
    name : Optional[str] = Field(...)
    email : Optional[str] = Field(...)
    password: Optional[str] = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "name" : "Name",
                "email": "abcdef@x.com",
                "password": "Password@67"
                
            }
        }