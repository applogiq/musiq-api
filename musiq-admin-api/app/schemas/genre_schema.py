from pydantic import BaseModel,Field
from typing import Dict

###to enter genre details schema
class GenreSchema(BaseModel):
    genre_name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "genre_name" : "Hip pop"
            }
        }