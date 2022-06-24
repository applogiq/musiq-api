from pydantic import BaseModel,Field
from typing import Dict

class CategorySchema(BaseModel):
    category_name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "category_name" : "Comedy"
            }
        }