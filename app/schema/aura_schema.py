from pydantic import BaseModel,Field
from typing import Dict,Optional


class AuraSchema(BaseModel):
    name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "name" : "Melody"
            }
        }

class AuranewSchema(BaseModel):
    name : str = Field(...)
    image: Optional[str] = None 
    class Config:
        schema_extra = {
            "example":{
                "name" : "Melody",
                "image" : "dfjhfhwerfhdfnslfwerwijerdjl"
            }
        }
