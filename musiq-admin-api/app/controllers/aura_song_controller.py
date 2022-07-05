from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.aura_song_service import *


def get_all_aura_song_details(db,limit):
    db_aura = aura_song_get_all(db,limit)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : len(db_aura)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})


def get_aura_details_by_auraid(db,aura_id,limit):
    db_aura = aura_song_get_by_auraid(db,aura_id,limit)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : len(db_aura)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})
