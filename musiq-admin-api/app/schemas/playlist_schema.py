from pydantic import BaseModel,Field
from typing import Dict,Optional

###to create playlist particular user schema
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

###to update playlist name by it's id details
class UpdateSchema(BaseModel):
    name : str
    class Config:
        scheme_extra = {
            "name" : "new name"
        }


