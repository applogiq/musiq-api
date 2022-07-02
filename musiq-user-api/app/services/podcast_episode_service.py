from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
from pydub import AudioSegment
from mutagen.mp3 import MP3


from model.podcast_model import podcast
from model.podcast_episode_model import podcast_episode
from model.podcast_author_model import podcast_author
from model.category_model import categories
from config.database import DIRECTORY
from services.podcast_service import *

def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    mins = seconds // 60
    seconds %= 60
    return(str(round(hours)).zfill(2), str(round(mins)).zfill(2), str(round(seconds)).zfill(2))

def episode_audio_check(db,id):
    return  db.query(podcast_episode).filter(podcast_episode.id == id,podcast_episode.is_delete == False,podcast_episode.is_audio == True).first()

def get_podcast_name(id,db):
    return db.query(podcast).filter(podcast.id == id,podcast.is_delete == False).first()

def episode_name_check(id,title,db):
    print(3333)
    return db.query(podcast_episode).filter(podcast_episode.episode_title == title,podcast_episode.podcast_id == id,podcast_episode.is_delete == False).first()

def episode_get_all(db: Session,limit):
    return db.query(podcast_episode).filter(podcast_episode.is_delete == False).order_by(podcast_episode.id).limit(limit).all()

def episode_get_by_id(db: Session, id: int):
    print(33333333344444444444)
    return db.query(podcast_episode).filter(podcast_episode.id == id,podcast_episode.is_delete == False).first()

def episode_get_by_podcastid(db: Session, id: int,limit):
    print(333333333333333333333)
    return db.query(podcast_episode).filter(podcast_episode.podcast_id == id,podcast_episode.is_delete == False).order_by(podcast_episode.episode_number).limit(limit).all()

