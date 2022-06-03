from pydantic import BaseModel,Field
from typing import Dict,List
# from datetime import time,date

from app.schema.album_schema import Responsealbum

class SongSchema(BaseModel):
    song_name : str = Field(...)
    artist_id : Dict[str, list] = None
    album_id : str = Field(...)
    genre_id : Dict[str, list] = None
    duration: str = Field(...)
    lyrics: str = Field(...)
    released_date : str
    song_size : str
    label : str
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "song_name" : "Melody",
                "artist_id" :{"artist": ["data"]},
                "album_id" : "g001",
                "genre_id" : {"genres": ["data"]},
                "duration": "00:05:45",
                "lyrics": "mnfmsnfgj,fkjk,flsdkl",
                "released_date": "2020-05-01",
                "song_size" :"30MB",
                "label" : "Sony Production"
            }
        }
    

class Base64Schema(BaseModel):
    song = bytes 
    class Config:
        schema_extra = {
            "example":{
                "song" : "sdmfkfkfl"  
            }
        }

class SongResponse(SongSchema):
    song_id: str = Field(...)
    album_details: Responsealbum

    class Config:
        orm_mode = True




class AllresponseSchema(BaseModel):
    records: List[SongResponse] = []
    totalrecords: int
    success: bool
    class Config:
        orm_mode = True

class SongresponseSchema(BaseModel):
    records: SongResponse
    totalrecords: int
    success: bool
    class Config:
        orm_mode = True
