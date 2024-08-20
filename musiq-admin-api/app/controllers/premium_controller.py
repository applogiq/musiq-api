from fastapi import HTTPException

from services.premium_service import *


###response of creating premium detail
def create_premium_details(db,premium_name,email):
    temp = premium_details(db,premium_name,email)
    if temp:
        return {"success":True,'message': "premium details added","records": temp}
    else:
        return {'message': "check your details","success": False}

###response of getting all premium details
def get_all_premium(db,limit):
    try:
        users = premium_get_all(db,limit)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"success":True,"message": "fetched successfully","records": users,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})

        
###response of fetching detail of particular premium
def get_premium_by_id(db,id):
    premium = premium_get_by_id(db,id)
    if premium:
        return {"success":True,"message":"details fetched successfully","records": premium,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

###response of updating existing premium detail
def update_premium(db,id,premium,email):
    db_premium = premium_update(db,id,premium,email)
    if db_premium:
        return {"status": True,"message":"premium details updated Successfully","records":db_premium}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "premium details doesn't exist"})

###response for delete the premium detail
def delete_premium(db,premium_id):
    db_premium = premium_delete(db,premium_id)
    if db_premium:
        return {"status": True,"message":"premium details deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "premium details doesn't exist"})