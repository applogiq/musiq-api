import urllib
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import databases
import socket
from decouple import config



##########################DATABASE CONNECTION#############################

host_server = os.environ.get('host_server', 'localhost')
db_server_port = urllib.parse.quote_plus(str(os.environ.get('db_server_port', '5432')))
database_name = os.environ.get('database_name', 'musiq')
db_username = urllib.parse.quote_plus(str(os.environ.get('db_username', 'postgres')))
db_password = urllib.parse.quote_plus(str(os.environ.get('db_password', '12345678')))#Applogiq123
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
##########################DATABASE CONNECTION#############################

############GETTING IPADDRESS#############
app_password = config("APP_PASSWORD")
hostname=socket.gethostname()
IPAddr=socket.gethostbyname(hostname)
############GETTING IPADDRESS#############
        

####SPECIFY STATIC FILE ROUTE####
# DIRECTORY = "/var/www/musiq-api/public"

DIRECTORY = "D:/Srimathi/Project/MusiQ/musiq-api/public"

