from fastapi import FastAPI
import uvicorn

from config.database import *
from routers import podcast_episode_routers,podcast_history_routers,playlist_song_routers,podcast_routers,aura_song_routers,aura_routers,favourite_routers,user_routers,artist_routers,album_routers,song_routers,recent_routers,last_song_routers,playlist_routers

##### Customizing our swagger 
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
        


app.include_router(user_routers.router)
app.include_router(artist_routers.router)
app.include_router(album_routers.router)
app.include_router(song_routers.router)
app.include_router(recent_routers.router)
app.include_router(last_song_routers.router)
app.include_router(favourite_routers.router)
app.include_router(playlist_routers.router)
app.include_router(playlist_song_routers.router)
app.include_router(aura_routers.router)
app.include_router(aura_song_routers.router)
app.include_router(podcast_routers.router)
app.include_router(podcast_episode_routers.router)
app.include_router(podcast_history_routers.router)

app.mount("/api/v1",app)

#####to show error occurance detail in swagger instead of "internal server"
@app.exception_handler(Exception) 
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}) 

####to enable static file control
app.mount("/public", StaticFiles(directory=DIRECTORY), name="public")


#####to run the program
if __name__ == "__main__":
    uvicorn.run("main:app",port = 3000,reload=True)

