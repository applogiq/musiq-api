from databases import Database
from fastapi import Depends, FastAPI,Request
from imp import reload
# from matplotlib import artist
import uvicorn
import warnings
from sqlalchemy import exc as sa_exc


from config.database import *
from model.song_model import *
from routers import admin_user_routers
from routers import podcast_author_routers,category_routers,aura_song_routers,user_routers,aura_routers,artist_routers,album_routers,song_routers,genre_routers,last_song_routers,recent_routers,favourite_routers,playlist_routers,playlist_song_routers

from model.podcast_author_model import *
from model.podcast_episode_model import *
from model.podcast_model import *
from model.category_model import *
from model.podcast_recent_model import *
# app = database.app

app = FastAPI(title="Music Streaming API",
              description="This is a very custom OpenAPI schema",
              version="2.5.0",
              docs_url='/api/v1/docs',
              redoc_url='/api/v1/redoc',
              openapi_url='/openapi.json',
              servers=[
                        {"url": "https://example.com", "description": "Staging environment"},
                        # {"url": "https://prod.example.com", "description": "Production environment"},
                    ],
                    root_path="/api/v1")

app.include_router(admin_user_routers.router)
app.include_router(user_routers.router)
app.include_router(artist_routers.router)
app.include_router(album_routers.router)
app.include_router(song_routers.router)
app.include_router(genre_routers.router)
app.include_router(last_song_routers.router)
app.include_router(recent_routers.router)
app.include_router(favourite_routers.router)
app.include_router(playlist_routers.router)
app.include_router(playlist_song_routers.router)
app.include_router(aura_routers.router)
app.include_router(aura_song_routers.router)
app.include_router(category_routers.router)
app.include_router(podcast_author_routers.router)

app.mount("/public", StaticFiles(directory=DIRECTORY), name="public")
        
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)
app.mount("/api/v1",app)

@app.exception_handler(Exception) 
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}) 

if __name__ == "__main__":
    uvicorn.run("main:app",host = IPAddr,port = 2000,reload=True)