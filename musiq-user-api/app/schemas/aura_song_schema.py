from pydantic import BaseModel

###to enter song for current mood detail schema
class AurasongSchema(BaseModel):
    aura_id : int
    song_id: int
    class Config:
        schema_extra = {
            "example":{
                "aura_id" : 1,
                "song_id" : 1
            }
        }
    
