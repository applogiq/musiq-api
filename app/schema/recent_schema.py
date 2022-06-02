from pydantic import BaseModel,Field
from typing import Dict,Optional

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