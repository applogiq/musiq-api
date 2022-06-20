from pydantic import BaseModel,Field
from typing import Dict,Optional


class LastSchema(BaseModel):
    user_id : int = Field(...)
    song_id : int = Field(...)
    paused_timing : str = Field(...)
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "user_id" : 202201,
                "song_id" : 1,
                "paused_timing": "00:02:00"
            }
        }