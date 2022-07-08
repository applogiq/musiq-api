from pydantic import BaseModel,Field
from typing import Dict,Union,List,Optional


class PodcastAuthorSchema(BaseModel):
    name : str
    image: Optional[str] = Field(...) 
    class Config:
        schema_extra = {
            "example": {
                    "name" :"new_name",
                    "image" : "dkfnsndfisdfhdfn"
            }
        }