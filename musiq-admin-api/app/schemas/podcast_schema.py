from pydantic import BaseModel,Field
from typing import Dict,List,Optional,Union
# from datetime import time,date


###to enter podcase details schema
class PodcastSchema(BaseModel):
    title : str = Field(...)
    description : str = Field(...)
    author_id : list = None
    category_id : list = None
    image: Optional[str] = Field(...)
    
    class Config:
        # orm_mode = True
        schema_extra = {
            "example":{
                "title" : "My podcast name",
                "description" :"This is my podcast",
                "author_id" : [1,2],
                "category_id" : [1,2],
                "image" : "dkfnsndfisdfhdfn"
            }
        }

###to update podcast details schema
class PodcastOptionalSchema(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    author_id : Optional[list] = None
    category_id : Optional[list] = None
    image: Optional[str] = Field(...)
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example":{
                "title" : "My podcast name",
                "description" :"This is my podcast",
                "author_id" : [1,2],
                "category_id" : [1,2],
                "image" : "dkfnsndfisdfhdfn"
            }
        }