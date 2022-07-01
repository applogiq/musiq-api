from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
import os


from model.podcast_model import podcast
from model.podcast_history_model import podcast_history
from model.podcast_episode_model import podcast_episode
from services.admin_user_service import admin_get_email
from config.database import DIRECTORY
from services.podcast_author_service import *

def podcast_history_detail(db: Session,history,email):
    # historyname =db.query(historyourites).filter(historyourites.user_id == history.user_id,historyourites.song_id == history.song_id).first()
    # if historyname:
    #     raise HTTPException(status_code=400, detail={"success": False,"message":"this song is already register for this user"}) 

    temp = admin_get_email(email,db)
    db_history = podcast_history(user_id = history.user_id,
                        podcast_id = history.podcast_id,
                        episode_number = history.episode_number,
                        paused_timing = history.paused_timing,
                        created_by = temp.id,
                        created_at = datetime.now()
                        )

    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history