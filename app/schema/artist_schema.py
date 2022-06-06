from pydantic import BaseModel,Field
from typing import Dict


class ArtistSchema(BaseModel):
    name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "name" : "AR Rahman"
            }
        }

class ArtistnewSchema(BaseModel):
    name : str = Field(...)
    image: bytes
    class Config:
        schema_extra = {
            "example":{
                "name" : "AR Rahman",
                "image": "ndfjweoijwnfkmsdfnifjsdfmsndfka"
            }
        }