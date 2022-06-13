from databases import Database
from fastapi import Depends, FastAPI,Request
from fastapi.responses import JSONResponse
from imp import reload
import uvicorn
from routers import user_routers,artist_routers
# from app.routers import user_routers

from config.database import *

# app = database.app
app.include_router(user_routers.router)
app.include_router(artist_routers.router)

app.mount("/api/v1",app)

@app.exception_handler(Exception) # exception handling api
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"}) 

if __name__ == "__main__":
    uvicorn.run("main:app",host = IPAddr,port = 3000,reload=True)