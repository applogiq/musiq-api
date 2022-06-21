from pydantic import BaseModel,Field
from typing import Dict,Optional

class ArtistSchema(BaseModel):
    artist_name : str = Field(...)
    image: Optional[str]
    class Config:
        schema_extra = {
            "example":{
                "artist_name" : "AR Rahman",
                "image": "ndfjweoijwnfkmsdfnifjsdfmsndfka"
            }
        }