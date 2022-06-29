from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64



# from utils.auth_handler import create_access_token
from model.demo_genre_model import *
from config.database import *
from model.album_model import *
from services.admin_user_service import *
from services.album_service import *

def demo_check(db):
    # query1 = db.query(songs).filter(songs.is_delete == False).all()
    query1 = db.query(demo_genre).all()
    # query1 = db.query(songs.id, songs.name).filter(songs.artist_id[0].in_([artist_id])).all()
    #query1 = db.query(songs.album_id, songs.name).filter(songs.artist_id.in_([1,2])).all()
    # print(query1[1].artist_id)
    # if 1 in query1[1].artist_id:
    #     print(True)
    # print(query1)

    return query1

# import wave
# import contextlib
# fname = f"{DIRECTORY}/music/tamil/Mis/3/songs/SG001.wav"
# with contextlib.closing(wave.open(fname,'r')) as f:
#     frames = f.getnframes()
#     rate = f.getframerate()
#     duration = frames / float(rate)
#     print(duration)