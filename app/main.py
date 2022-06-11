from databases import Database
from fastapi import Depends, FastAPI,Request
from imp import reload
import uvicorn
from routers import user_routers
# from app.routers import user_routers

from config.database import *

# app = database.app
app.include_router(user_routers.router)

app.mount("/api/v1",app)

if __name__ == "__main__":
    uvicorn.run("main:app",host = IPAddr,port = 3000,reload=True)