from pydantic import BaseModel,Field


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
    