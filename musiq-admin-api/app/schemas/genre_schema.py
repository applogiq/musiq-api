from pydantic import BaseModel,Field
from typing import Dict

class GenreSchema(BaseModel):
    name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "name" : "Hip pop"
            }
        }