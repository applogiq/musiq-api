from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from model.song_model import songs
from model.aura_model import aura
from model.aura_song_model import aura_songs
from services.admin_user_service import admin_get_email

def aura_song_detail(db: Session,auras,email):
    auraname =db.query(aura_songs).filter(aura_songs.aura_id == auras.aura_id,aura_songs.song_id == auras.song_id,aura_songs.is_delete == False).first()
    if auraname:
        raise HTTPException(status_code=400, detail="This song is already register for this aura") 
    
    temp1 = admin_get_email(email,db)
    
    db_aura = aura_songs(aura_id = auras.aura_id,
                        song_id = auras.song_id,
                        is_active = True,
                        is_delete = False,
                        created_by = temp1.id
                        )
    
    temp = db.query(aura).filter(aura.id == auras.aura_id,aura.is_delete == False).first()
    if temp:
        s = temp.no_of_songs 
        temp.no_of_songs = s+1

    db.add(db_aura)
    db.commit()
    db.refresh(db_aura)
    return {"message":"data added"}

def aura_song_get_all(db: Session):
    auras = db.query(aura_songs).filter(aura_songs.is_delete == False).all()
    if auras:
        return auras
    else:
        return False

def aura_song_get_by_id(db: Session, aura_id: int):
    auras = db.query(aura_songs).filter(aura_songs.id == aura_id,aura_songs.is_delete == False).first()
    if auras:
        return auras
    else:
        return False

def aura_song_get_by_auraid(db: Session, aura_id: str):
    auras = db.query(aura_songs).filter(aura_songs.aura_id.in_([aura_id]),aura_songs.is_delete == False).all()
    return auras

def aura_song_delete(db: Session,aura_id):
    user_temp = db.query(aura_songs).filter(aura_songs.id == aura_id,aura_songs.is_delete == False).first()
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="aura details doesn't exist")