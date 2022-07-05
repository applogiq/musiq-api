from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
import os


from model.podcast_model import podcast
from config.database import DIRECTORY
# from services.podcast_author_service import *


def podcast_name_check(title,db):
    return db.query(podcast).filter(podcast.title == title,podcast.is_delete == False).first()

def podcast_get_all(db: Session,limit):
    return db.query(podcast).filter(podcast.is_delete == False).order_by(podcast.id).limit(limit).all()

def podcast_get_by_id(db: Session, id: int):
    return db.query(podcast).filter(podcast.id == id,podcast.is_delete == False).first()

