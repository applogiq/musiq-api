from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date


class EpisodeSchema(BaseModel):
    podcast_id : int = Field(...)
    episode_title : str = Field(...)
    description : str = Field(...)
    subtitles: str = Field(...)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "podcast_id" : 1,
                "episode_title" : "My podcast name",
                "description" :"This is my podcast",
                "subtitles" : "ndfndfnm dmnd cmncn ndfmsdnf ndjdcns" 
            }
        }

class EpisodeOptinalSchema(BaseModel):
    podcast_id : Optional[int] = None
    episode_number : Optional[str] = None
    episode_title : Optional[str] = None
    description : Optional[str] = None
    subtitles: Optional[str] = None