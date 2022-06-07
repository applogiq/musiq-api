import urllib
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import databases
from fastapi.openapi.utils import get_openapi

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'music1')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', '12345678')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode', 'prefer')))

DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(db_username, db_password, host_server, db_server_port, database_name, ssl_mode)
SQLALCHEMY_TRACK_MODIFICATIONS = False

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# def custom_openapi(app):
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Music Streaming API",
#         version="2.5.0",
#         description="This is a very custom OpenAPI schema",
#         routes= app.routes,
#     )
#     # openapi_schema["info"]["x-logo"] = {
#     #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#     # }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema