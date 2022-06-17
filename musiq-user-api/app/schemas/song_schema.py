from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date

from schemas.album_schema import Responsealbum


class SongResponse(BaseModel):
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