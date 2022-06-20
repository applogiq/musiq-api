from databases import Database
from fastapi import Depends, FastAPI,Request
from imp import reload
# from matplotlib import artist
import uvicorn


# from app.routers import user_routers

from config.database import *
# from model.admin_user_model import *
from routers import user_routers,artist_routers,album_routers,song_routers,recent_routers,last_song_routers


# app = database.app


app.include_router(user_routers.router)
app.include_router(artist_routers.router)
app.include_router(album_routers.router)
app.include_router(song_routers.router)
app.include_router(recent_routers.router)
app.include_router(last_song_routers.router)

app.mount("/api/v1",app)

@app.exception_handler(Exception) 
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}) 


if __name__ == "__main__":
    uvicorn.run("main:app",host = IPAddr,port = 3000,reload=True)

