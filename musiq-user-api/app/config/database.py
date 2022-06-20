import urllib
import os,sys
from pyparsing import Diagnostics
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import databases
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import socket
from fastapi.staticfiles import StaticFiles
from decouple import config

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'music')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', '12345678')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
SQLALCHEMY_TRACK_MODIFICATIONS = False

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app_password = config("APP_PASSWORD")
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
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
        

DIRECTORY = "D:\Srimathi\Project\MusiQ\public"
# script_dir = os.path.dirname(__file__)
# os.chdir("MusicQ/public")
# st_abs_file_path = 
# script_dir = sys.path.append('\MusiQ\public')
# print(script_dir)
# impath = os.path.join(script_dir, '..\MusiQ\public')

app.mount("/public", StaticFiles(directory=DIRECTORY), name="public")
        
# app = FastAPI(title="Music Streaming API",
#         version="2.5.0",
#         description="This is a very custom OpenAPI schema")

