from pydantic import BaseModel

###to enter favourite song of particular user detail schema
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