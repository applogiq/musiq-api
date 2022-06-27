from pydantic import BaseModel,Field
from typing import Dict,Union,List,Optional


class PodcastAuthorSchema(BaseModel):
    author : str
    class Config:
        schema_extra = {
            "example": {
                    "author" :"{'author_name': 'name'}"
            }
        }