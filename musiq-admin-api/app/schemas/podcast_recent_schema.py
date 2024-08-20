from pydantic import BaseModel,Field
from typing import Dict,Optional,List

# from schemas.user_schema import UserResponse

class PodcastRecentSchema(BaseModel):
    user_id : int = Field(...)
    podcast_id : int
    episode_id : int
    paused_timing: str
    class Config:
        schema_extra = {
            "example":{
                "user_id" : 202201,
                "podcast_id" : 1,
                "episode_id" : 1,
                "paused_timing" : "00:02:45"
            }
        }
