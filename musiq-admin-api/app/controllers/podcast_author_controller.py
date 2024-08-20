from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.podcast_author_service import *

###response of creating author details 
def create_author_details(db,author_name,email):
    temp = author_details(db,author_name,email)
    if temp:
        return {"success":True,'message': "author details added","records": temp}
    else:
        return {'message': "check your details","success": False}

###response of get all author details
def get_all_author(db,limit):
    try:
        users = author_get_all(db,limit)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"success":True,"message": "fetched successfully","records": users,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})

###response for getting particular author details by their id
def get_author_by_id(db,id):
    author = author_get_by_id(db,id)
    if author:
        return {"success":True,"message":"details fetched successfully","records": author,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


###response of updating existing author details 
def update_author(db,gen_id,author,email):
    db_author = author_update(db,gen_id,author,email)
    if db_author:
        return {"status": True,"message":"author details updated Successfully","records":db_author}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "author details doesn't exist"})

###response of deleting author detail
def delete_author(db,author_id):
    db_author = author_delete(db,author_id)
    if db_author:
        return {"status": True,"message":"author details deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "author details doesn't exist"})
