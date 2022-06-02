from pydantic import BaseModel,Field
from typing import Dict,Optional

class LastSchema(BaseModel):
    user_id : int = Field(...)
    song_id : str = Field(...)
    paused_timing : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "user_id" : 220202,
                "song_id" : "SG001",
                "paused_timing": "00:02:00"
            }
        }