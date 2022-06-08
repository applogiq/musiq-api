from pydantic import BaseModel,Field
from typing import Dict,Optional


class PlaylistSchema(BaseModel):
    user_id : int
    name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "user_id": 1,
                "name" : "Melody"
            }
        }


