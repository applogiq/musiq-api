from sqlalchemy.orm import Session
from datetime import datetime
import shutil
import base64
from fastapi import HTTPException
import os

from app.model.song_model import songs
from app.model.aura_model import aura
from app.model.aura_song_model import aura_songs

def aura_song_detail(db: Session,auras):
    auraname =db.query(aura_songs).filter(aura_songs.aura_id == auras.aura_id,aura_songs.song_id == auras.song_id,aura_songs.is_delete == 0).first()
    if auraname:
        raise HTTPException(status_code=400, detail="This song is already register for this aura") 
    else:
        db_aura = aura_songs(aura_id = auras.aura_id,
                            song_id = auras.song_id,
                            is_active = 1,
                            is_delete = 0,
                            updated_by = 0,
                            created_by = 1
                            )

        db.add(db_aura)
        db.commit()
        db.refresh(db_aura)
        return {"message":"data added"}

    
def get_aura_song(db: Session, aura_id: int):
    auras = db.query(aura_songs).filter(aura_songs.id == aura_id,aura_songs.is_delete == 0).first()
    if auras:
        return auras
    else:
        return False

def get_aura_songs(db: Session):
    auras = db.query(aura_songs).filter(aura_songs.is_delete == 0).all()
    if auras:
        return auras
    else:
        return False

def aura_song_delete(db: Session,aura_id):
    user_temp = db.query(aura_songs).filter(aura_songs.id == aura_id,aura_songs.is_delete == 0).first()
    if user_temp:
        user_temp.is_delete = 1
        db.commit()
        return {"message":"Deleted"}
    else:
        # return {"message":"aura details doesn't exist"}
        raise HTTPException(status_code=404, detail="aura details doesn't exist")

def aura_song_fetch(db: Session, aura_id: str):
    user_temp = db.query(aura_songs).filter(aura_songs.is_delete == 0).first()
    # s = []
    # print(len(user_temp))
    # for i in range(0,len(user_temp)):
    #     user_temp = db.query(aura_songs).filter(user[i].aura_id == aura_id,aura_songs.is_delete == 0).first()
    #     s.append(user_temp.song_id)
    return user_temp

