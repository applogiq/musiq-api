from pydantic import BaseModel,Field
from typing import Dict,Union,List,Optional


class PodcastAuthorSchema(BaseModel):
    author_name : Optional[str]
    image : Optional[str]
    class Config:
        schema_extra = {
            "example":{
                "author_name" : "Movie name",
                "image" : "hbdhebrjherhwejrdsdsmfsmdf"
            }
        }