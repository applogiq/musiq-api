from pydantic import BaseModel,Field
from typing import List

###to enter recent song details for particular user schema
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

###base recent response schema
class Recentresponse(BaseModel):
    user_id : int = Field(...)
    song_id : dict = Field(...)

    class Config:
        orm_mode = True

###get all user's recent list schema
class AllrecentSchema(BaseModel):
    records: List[Recentresponse] = []
    totalrecords: int
    success: bool
    class Config:
        orm_mode = True

# class RecentresponseSchema(BaseModel):
#     records: Recentresponse
#     totalrecords: int
#     success: bool

#     class Config:
#         orm_mode = True