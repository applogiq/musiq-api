from databases import Database
from fastapi import Depends, FastAPI,Request
from imp import reload
# from matplotlib import artist
import uvicorn

# from app.routers import user_routers

from config.database import *
from model.song_model import *
from routers import admin_user_routers
from routers import user_routers,artist_routers,album_routers,song_routers

# app = database.app

app.include_router(admin_user_routers.router)
app.include_router(user_routers.router)
app.include_router(artist_routers.router)
app.include_router(album_routers.router)
app.include_router(song_routers.router)

app.mount("/api/v1",app)

if __name__ == "__main__":
    uvicorn.run("main:app",host = IPAddr,port = 2000,reload=True)