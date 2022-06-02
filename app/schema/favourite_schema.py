from pydantic import BaseModel,Field


class FavouriteSchema(BaseModel):
    user_id : int
    song_id: str
    class Config:
        schema_extra = {
            "example":{
                "user_id" : 202201,
                "song_id" : "SG001"
            }
        }