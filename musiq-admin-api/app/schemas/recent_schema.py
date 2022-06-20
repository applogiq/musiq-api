from pydantic import BaseModel,Field
from typing import Dict,Optional,List

# from schemas.user_schema import UserResponse

class RecentSchema(BaseModel):
    user_id : int = Field(...)
    song_id : int
    class Config:
        schema_extra = {
            "example":{
                "user_id" : 202201,
                "song_id" : 1
            }
        }

class Recentresponse(BaseModel):
    user_id : int = Field(...)
    song_id : dict = Field(...)

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