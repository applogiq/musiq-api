from pydantic import BaseModel,Field
from typing import Dict,Optional

class ArtistSchema(BaseModel):
    name : str = Field(...)
    image: Optional[str]
    class Config:
        schema_extra = {
            "example":{
                "name" : "AR Rahman",
                "image": "ndfjweoijwnfkmsdfnifjsdfmsndfka"
            }
        }