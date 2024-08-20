from pydantic import BaseModel,Field


###to enter song in particular playlist details
class PlaylistsongSchema(BaseModel):
    playlist_id : int
    song_id: int
    class Config:
        schema_extra = {
            "example":{
                "playlist_id" : 1,
                "song_id" : 1
            }
        }
    