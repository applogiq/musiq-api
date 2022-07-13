from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date

from schemas.album_schema import Responsealbum

###song response schema
class SongResponse(BaseModel):
    song_name : str = Field(...)
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

###get all song response schema
class AllresponseSchema(BaseModel):
    success: bool
    message: str
    records: List[SongResponse] = []
    totalrecords: int
    class Config:
        orm_mode = True

##get song details by it's id schema
class SongresponseSchema(BaseModel):
    success: bool
    message: str
    records: SongResponse
    totalrecords: int
    class Config:
        orm_mode = True