from pydantic import BaseModel,Field
from typing import Dict,Optional

from schema.user_schema import UserSchema
# from app.schema.song_schema import 

class LastSchema(BaseModel):
    user_id : int = Field(...)
    song_id : str = Field(...)
    paused_timing : str = Field(...)
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "user_id" : 220202,
                "song_id" : "SG001",
                "paused_timing": "00:02:00"
            }
        }

class Recentresponse(BaseModel):
    user_id : int = Field(...)
    song_id : dict = Field(...)

    class Config:
        orm_mode = True

