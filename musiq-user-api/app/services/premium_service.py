from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException
import shutil
from typing import Optional
import os


from model.premium_status_model import premium
from config.database import DIRECTORY
# from services.premium_author_service import *

###get all premium details
def premium_get_all(db: Session,limit):
    return db.query(premium).filter(premium.is_delete == False).order_by(premium.id).limit(limit).all()

###get single premium details by id
def premium_get_by_id(db: Session, id: int):
    return db.query(premium).filter(premium.id == id,premium.is_delete == False).first()

