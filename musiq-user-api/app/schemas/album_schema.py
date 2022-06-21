from pydantic import BaseModel,Field
from typing import Dict,Union,List,Optional


class AlbumSchema(BaseModel):
    album_name : Optional[str]
    released_year : Optional[str]
    music_director :list = None
    image : Optional[str]
    class Config:
        schema_extra = {
            "example":{
                "album_name" : "Movie name",
                "released_year" : "2009",
                "music_director" : [1,2],
                "image" : "hbdhebrjherhwejrdsdsmfsmdf"
            }
        }

class Responsealbum(BaseModel):
    album_id : str
    no_of_songs: int
    album_name : str
    released_year : int
    music_director : list = None 
    music_director_name : list = None
    is_image : int

    class Config:
        orm_mode = True

class AlbumResponse(BaseModel):
    success: bool
    message: str
    records: Responsealbum 
    totalrecords: int
    

    class Config:
        orm_mode = True

class AllalbumResponse(BaseModel):
    success: bool
    message: str
    records: List[Responsealbum] = []
    totalrecords: int
    
    
    class Config:
        orm_mode = True
