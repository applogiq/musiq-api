from pydantic import BaseModel,Field
from typing import Dict,Optional

###to create new current mood category details schema
class AuraSchema(BaseModel):
    aura_name : str = Field(...)
    image: Optional[str] = None 
    class Config:
        schema_extra = {
            "example":{
                "aura_name" : "Melody",
                "image" : "dfjhfhwerfhdfnslfwerwijerdjl"
            }
        }
