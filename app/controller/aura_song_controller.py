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

def aura_song_fetch(db: Session, aura_id: str):
    auras = db.query(aura_songs).filter(aura_songs.is_delete == 0).all()
    s = []
    print(len(auras))
    for i in range(0,len(auras)):
        if auras[i].aura_id == aura_id:
            s.append(auras[i].song_id)
        else:
            raise HTTPException(status_code=404, detail="No song is register for this aura.Check your id!!!") 
    return s

def aura_song_update(db,aura_id,auras):
    user_temp = db.query(aura_songs).filter(aura_songs.id == aura_id,aura_songs.is_delete == 0).first()
    if user_temp:
        if auras.aura_id:
            user_temp.aura_id = auras.aura_id
        if auras.song_id:
            user_temp.song_id = auras.song_id
        
        user_temp.updated_by = 1
        user_temp.updated_at = datetime.now()
        db.commit()
        return {'message': "data updated"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")

def aura_song_delete(db: Session,aura_id):
    user_temp = db.query(aura_songs).filter(aura_songs.id == aura_id,aura_songs.is_delete == 0).first()
    if user_temp:
        user_temp.is_delete = 1
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")

