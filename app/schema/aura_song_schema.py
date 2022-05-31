from pydantic import BaseModel,Field


class AurasongSchema(BaseModel):
    aura_id : str = Field(...)
    song_id: str
    class Config:
        schema_extra = {
            "example":{
                "aura_id" : "AUR001",
                "song_id" : "SG001"
            }
        }