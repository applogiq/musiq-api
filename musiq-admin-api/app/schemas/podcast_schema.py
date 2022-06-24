from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date


class PodcastSchema(BaseModel):
    title : str = Field(...)
    description : str = Field(...)
    subtitles: str = Field(...)
    author_id : list = None
    category_id : list = None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "title" : "My podcast name",
                "description" :"This is my podcast",
                "subtitles" : "ndfndfnm dmnd cmncn ndfmsdnf ndjdcns",
                "author_id" : [1,2],
                "category_id" : [1,2]
            }
        }