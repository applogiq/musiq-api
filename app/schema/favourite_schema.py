from pydantic import BaseModel,Field


class FavouriteSchema(BaseModel):
    user_id : int
    song_id: int
    class Config:
        schema_extra = {
            "example":{
                "user_id" : 1,
                "song_id" : 1
            }
        }