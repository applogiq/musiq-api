from fastapi import Depends, FastAPI
from imp import reload
import uvicorn
import sqlalchemy
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from fastapi.openapi.utils import get_openapi


from app.model.user_model import users
from app.model.song_model import songs
from app.model.recent_model import recents
from app.model.last_song_model import last_songs
from app.model.genre_model import genres
from app.model.favourite_model import favourites
from app.model.aura_model import aura
from app.model.aura_song_model import aura_songs
from app.model.artist_model import artist
from app.model.album_model import albums
# from app.model.recent_model import recents
from app.routers import user_routers,song_routers,artist_routers,genre_routers,album_routers,last_song_routers,aura_routers,aura_song_routers,recent_routers,favourite_routers


from app.config.database import custom_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Music Streaming API",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes= app.routes,
    )
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# app.openapi = custom_openapi

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

app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)



if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)