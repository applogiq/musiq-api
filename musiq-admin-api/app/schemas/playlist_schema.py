from pydantic import BaseModel,Field
from typing import Dict,Optional


class PlaylistSchema(BaseModel):
    user_id : int
    playlist_name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "user_id": 1,
                "playlist_name" : "Melody"
            }
        }

class UpdateSchema(BaseModel):
    name : str
    class Config:
        scheme_extra = {
            "name" : "new name"
        }


