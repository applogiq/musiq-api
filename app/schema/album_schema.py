from pydantic import BaseModel,Field
from typing import Dict,Union,List,Optional

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

class AlbumnewSchema(BaseModel):
    name : str = Field(...)
    released_year : int 
    music_director : Union[str, None] = None 
    image : Optional[str]
    class Config:
        schema_extra = {
            "example":{
                "name" : "Movie name",
                "released_year" : 2009,
                "music_director" : "AL00DOC",
                "image" : "hbdhebrjherhwejrdsdsmfsmdf"
            }
        }

class Responsealbum(AlbumSchema):
    album_id : str
    no_of_songs: int

    class Config:
        orm_mode = True

class AlbumResponse(BaseModel):
    records: Responsealbum 
    totalrecords: int
    success: bool

    class Config:
        orm_mode = True

class AllalbumResponse(BaseModel):
    records: List[Responsealbum] = []
    totalrecords: int
    success: bool
    
    class Config:
        orm_mode = True

