from pydantic import BaseModel,Field
from typing import Dict

class GenreSchema(BaseModel):
    genre_name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "genre_name" : "Hip pop"
            }
        }