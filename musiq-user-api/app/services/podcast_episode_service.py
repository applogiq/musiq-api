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

###to check presence of any episode
def episode_audio_check(db,id):
    return  db.query(podcast_episode).filter(podcast_episode.id == id,podcast_episode.is_delete == False,podcast_episode.is_audio == True).first()

###get all episodes of all podcast
def episode_get_all(db: Session,limit):
    return db.query(podcast_episode).filter(podcast_episode.is_delete == False).order_by(podcast_episode.id).limit(limit).all()

###get episode by its id
def episode_get_by_id(db: Session, id: int):
    return db.query(podcast_episode).filter(podcast_episode.id == id,podcast_episode.is_delete == False).first()

###get all episode detail for particular podcast by id
def episode_get_by_podcastid(db: Session, id: int,limit):
    return db.query(podcast_episode).filter(podcast_episode.podcast_id == id,podcast_episode.is_delete == False).order_by(podcast_episode.episode_number).limit(limit).all()

