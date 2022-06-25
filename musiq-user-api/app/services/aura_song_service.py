from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from model.song_model import songs
from model.aura_model import aura
from model.aura_song_model import aura_songs


def aura_song_get_all(db: Session,limit):
    auras = db.query(aura_songs).filter(aura_songs.is_delete == False).limit(limit).all()
    if auras:
        return auras
    return False

def aura_song_get_by_auraid(db: Session, aura_id: str,limit):
    auras = db.query(aura_songs).filter(aura_songs.aura_id.in_([aura_id]),aura_songs.is_delete == False).limit(limit).all()
    return auras

