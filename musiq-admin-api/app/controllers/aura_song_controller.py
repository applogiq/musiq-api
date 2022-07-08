from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.aura_song_service import *

def create_aura_song_details(db,auras,email):
    db_aura = aura_song_detail(db,auras,email)
    if db_aura:
        return {"success":True,"message": "song uploaded successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})

def get_all_aura_song_details(db):
    db_aura = aura_song_get_all(db)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : len(db_aura)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_aura_details_by_id(db,aura_song_id):
    db_aura = aura_song_get_by_id(db,aura_song_id)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_aura_details_by_auraid(db,aura_id):
    db_aura = aura_song_get_by_auraid(db,aura_id)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : len(db_aura)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

def delete_aura_song(db,aura_song_id):
    db_aura = aura_song_delete(db,aura_song_id)
    if db_aura:
        return {"status": True,"message":"song removed from aura list"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "aura song details doesn't exist"})