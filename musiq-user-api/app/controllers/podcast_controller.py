from fastapi import HTTPException

from services.podcast_service import *



def get_all_podcast(db,limit):
    try:
        users = podcast_get_all(db,limit)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"success":True,"message": "fetched successfully","records": users,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})

        

def get_podcast_by_id(db,id):
    podcast = podcast_get_by_id(db,id)
    if podcast:
        return {"success":True,"message":"details fetched successfully","records": podcast,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})


