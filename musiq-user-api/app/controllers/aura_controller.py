from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.aura_service import *


def get_all_aura_details(db,limit):
    db_aura = aura_get_all(db,limit)
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






