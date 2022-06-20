from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date

from schemas.album_schema import Responsealbum


class SongSchema(BaseModel):
    name : str = Field(...)
    artist_id : list = None
    album_id : Union[str,None] = None
    genre_id : Dict[str, list] = None
    duration: str = Field(...)
    lyrics: str = Field(...)
    released_date : str
    song_size : str
    label : str
    music: Optional[str] = None
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "name" : "Melody",
                "artist_id" :[1,2],
                "album_id" : "g001",
                "genre_id" : {"genres": ["data"]},
                "duration": "00:05:45",
                "lyrics": "mnfmsnfgj,fkjk,flsdkl",
                "released_date": "2020-05-01",
                "song_size" :"30MB",
                "label" : "Sony Production",
                "music" : "sdmfkfkfl" 
            }
        }
    

class SongResponse(SongSchema):
    song_id: str = Field(...)
    album_details: Responsealbum

    class Config:
        orm_mode = True


class AllresponseSchema(BaseModel):
    success: bool
    message: str
    records: List[SongResponse] = []
    totalrecords: int
    class Config:
        orm_mode = True

class SongresponseSchema(BaseModel):
    success: bool
    message: str
    records: SongResponse
    totalrecords: int
    class Config:
        orm_mode = True