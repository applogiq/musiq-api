from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date


class PodcastSchema(BaseModel):
    title : str = Field(...)
    description : str = Field(...)
    author_id : list = None
    category_id : list = None
    
    class Config:
        # orm_mode = True
        schema_extra = {
            "example":{
                "title" : "My podcast name",
                "description" :"This is my podcast",
                "author_id" : [1,2],
                "category_id" : [1,2]
            }
        }

class PodcastOptionalSchema(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    author_id : Optional[list] = None
    category_id : Optional[list] = None
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "title" : "My podcast name",
                "description" :"This is my podcast",
                "author_id" : [1,2],
                "category_id" : [1,2]
            }
        }