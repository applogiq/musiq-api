from pydantic import BaseModel,Field
from typing import Dict,Union,List,Optional

###to enter new album details schema
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

###structure of response strcuture of album details schema
class Responsealbum(BaseModel):
    id: int
    album_id : str
    no_of_songs: int
    album_name : str
    released_year : int
    music_director : list = None
    music_director_name: list = None
    is_image : int

    class Config:
        orm_mode = True

###to get album response by their id schema
class AlbumResponse(BaseModel):
    success: bool
    message: str
    records: Responsealbum 
    totalrecords: int
    

    class Config:
        orm_mode = True

###to get all album details response schema
class AllalbumResponse(BaseModel):
    success: bool
    message: str
    records: List[Responsealbum] = []
    totalrecords: int   
    class Config:
        orm_mode = True
