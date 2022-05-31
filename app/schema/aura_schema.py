from pydantic import BaseModel,Field
from typing import Dict


class AuraSchema(BaseModel):
    name : str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "name" : "Melody"
            }
        }

class AurasongSchema(BaseModel):
    name : str = Field(...)
    song: list 
    class Config:
        schema_extra = {
            "example":{
                "aura_id" : "AUR001",
                "songs" : ["SG001","SG002","SG003"]
            }
        }