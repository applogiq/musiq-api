from fastapi import HTTPException

from services.premium_service import *


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

