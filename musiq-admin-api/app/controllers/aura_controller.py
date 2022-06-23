from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.aura_service import *

def create_aura_details(db,auras,email):
    db_aura = aura_detail(db,auras,email)
    if db_aura:
        return {"success":True,"message": "aura created successfully"}
    else:
        raise HTTPException(status_code=404, detail={"message": "check your details","success":False})

def get_all_aura_details(db):
    db_aura = aura_get_all(db)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : len(db_aura)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_aura_details_by_id(db, aura_id):
    db_aura = aura_get_by_id(db, aura_id)
    if db_aura:
        return {"success":True,"message":"details fetched succesfully","records": db_aura,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def update_aura_details(db: Session,aura_id: int,auras,email):
    db_aura = aura_update(db,aura_id,auras,email)
    if db_aura:
        return {"success": True,"message":"aura details updated Successfully","records":db_aura}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "aura details doesn't exist"})

def delete_aura_details(db,aura_id):
    db_aura = aura_delete(db,aura_id)
    if db_aura:
        return {"success": True,"message":"aura details deleted"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "aura details doesn't exist"})


def delete_aura_image(db,aura_id):
    db_aura = aura_image_delete(db,aura_id)
    if db_aura:
        return {"success": True,"message":"image removed from aura details"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "aura details doesn't exist"})

