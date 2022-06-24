from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.genre_service import *


def create_genre_details(db,genre,email):
    temp = genre_detail(db,genre,email)
    if temp:
        return {"success":True,'message': "song details added","records": temp}
    else:
        return {'message': "check your details","success": False}

def get_all_genre_details(db):
    try:
        temp = genre_get_all(db)
        return {"success":True,"message": {"genre details fetched successfully"},"records": temp,"total_records" : len(temp)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_genre_by_id(db, genre_id):
    db_genre = genre_get_by_id(db, genre_id)
    if db_genre:
        return {"success":True,"message":"Fetched successfully","records": db_genre,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

def update_genre(db,gen_id,genre,email):
    db_genre = genre_update(db,gen_id,genre,email)
    if db_genre:
        return {"status": True,"message":"genre details updated Successfully","records":db_genre}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "genre details doesn't exist"})

def delete_genre_details(db,genre_id):
    db_genre = genre_delete(db,genre_id)
    if db_genre:
        return {"status": True,"message":"genre details deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "genre details doesn't exist"})