from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from services.category_service import *

###response of creating category detail
def create_category_details(db,category,email):
    temp = category_detail(db,category,email)
    if temp:
        return {"success":True,'message': "song details added","records": temp}
    else:
        return {'message': "check your details","success": False}

###response of getting all category details
def get_all_category_details(db):
    try:
        temp = category_get_all(db)
        return {"success":True,"message": {"category details fetched successfully"},"records": temp,"total_records" : len(temp)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

###response of fetching detail of particular category
def get_category_by_id(db, category_id):
    db_category = category_get_by_id(db, category_id)
    if db_category:
        return {"success":True,"message":"Fetched successfully","records": db_category,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

###response of updating existing category detail
def update_category(db,cat_id,category,email):
    db_category = category_update(db,cat_id,category,email)
    if db_category:
        return {"status": True,"message":"category details updated Successfully","records":db_category}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "category details doesn't exist"})

###response for delete the category detail
def delete_category_details(db,category_id):
    db_category = category_delete(db,category_id)
    if db_category:
        return {"status": True,"message":"category details deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "category details doesn't exist"})