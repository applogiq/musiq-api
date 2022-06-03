from pydantic import BaseModel,Field
from typing import Dict,Optional,List

from app.schema.user_schema import UserResponse

class RecentSchema(BaseModel):
    user_id : int = Field(...)
    song_id : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "user_id" : 220202,
                "song_id" : "SG001"
            }
        }

class Recentresponse(BaseModel):
    user_id : int = Field(...)
    song_id : dict = Field(...)
    user_details : UserResponse

    class Config:
        orm_mode = True

class AllrecentSchema(BaseModel):
    records: List[Recentresponse] = []
    totalrecords: int
    success: bool
    class Config:
        orm_mode = True

class RecentresponseSchema(BaseModel):
    records: Recentresponse
    totalrecords: int
    success: bool

    class Config:
        orm_mode = True