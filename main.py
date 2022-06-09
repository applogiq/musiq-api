from urllib.parse import scheme_chars
from fastapi import Depends, FastAPI,Request
from imp import reload
import uvicorn
import sqlalchemy
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from fastapi.openapi.utils import get_openapi
import socket


# # from app.model import *
# from app.model.user_model import users
# from app.model.song_model import songs
# from app.model.recent_model import recents
# from app.model.last_song_model import last_songs
# from app.model.genre_model import genres
# from app.model.favourite_model import favourites
# from app.model.aura_model import aura
# from app.model.aura_song_model import aura_songs
from app.model.playlist_model import playlist
from app.model.playlist_song_model import playlist_songs
# from app.routers import user_routers,song_routers,artist_routers,genre_routers,album_routers,last_song_routers,aura_routers,aura_song_routers,recent_routers,favourite_routers

from app.routers import user_routers,song_routers,artist_routers,genre_routers,album_routers,last_song_routers,aura_routers,aura_song_routers,recent_routers,favourite_routers,playlist_routers
from app.routers import playlist_song_routers
# from app.config.database import custom_openapi

app = FastAPI(title="Music Streaming API",
        version="2.5.0",
        description="This is a very custom OpenAPI schema")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

app.include_router(user_routers.router)
app.include_router(song_routers.router)
app.include_router(artist_routers.router)
app.include_router(genre_routers.router)
app.include_router(album_routers.router)
app.include_router(last_song_routers.router)
app.include_router(aura_routers.router)
app.include_router(aura_song_routers.router)
app.include_router(recent_routers.router)
app.include_router(favourite_routers.router)
app.include_router(playlist_routers.router)
app.include_router(playlist_song_routers.router)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
    # 