from pydantic import BaseModel,Field
from typing import Dict

###to enter podcast category details schema
class CategorySchema(BaseModel):
    category_name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "category_name" : "Comedy"
            }
        }