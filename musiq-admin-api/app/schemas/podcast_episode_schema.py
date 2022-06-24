from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date


class PodcastSchema(BaseModel):
    podcast_id : int = Field(...)
    episode_number : str = Field(...)
    title : str = Field(...)
    description : str = Field(...)
    subtitles: str = Field(...)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "podcast_id" : 1,
                "episode_number" : 1,
                "title" : "My podcast name",
                "description" :"This is my podcast",
                "subtitles" : "ndfndfnm dmnd cmncn ndfmsdnf ndjdcns" 
            }
        }