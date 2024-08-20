from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
import os


from model.podcast_model import podcast
from config.database import DIRECTORY
# from services.podcast_author_service import *

###get all podcast details
def podcast_get_all(db: Session,limit):
    return db.query(podcast).filter(podcast.is_delete == False).order_by(podcast.id).limit(limit).all()

###get single podcast details by id
def podcast_get_by_id(db: Session, id: int):
    return db.query(podcast).filter(podcast.id == id,podcast.is_delete == False).first()

