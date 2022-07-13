from pydantic import BaseModel,Field
from typing import Dict,Optional

###to enter artist details schema
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