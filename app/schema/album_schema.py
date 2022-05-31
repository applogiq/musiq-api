from pydantic import BaseModel,Field
from typing import Dict,Union

class AlbumSchema(BaseModel):
    name : str = Field(...)
    released_year : int 
    music_director : Union[str, None] = None 
    class Config:
        schema_extra = {
            "example":{
                "name" : "Movie name",
                "released_year" : 2009,
                "music_director" : "AL00DOC"
            }
        }