from fastapi import HTTPException

from services.podcast_service import *

def create_podcast_details(db,podcast_name,email,uploaded_file = None):
    temp = podcast_details(db,podcast_name,email,uploaded_file)
    if temp:
        return {"success":True,'message': "podcast details added","records": temp}
    else:
        return {'message': "check your details","success": False}

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


def update_podcast(db,id,podcast,email,file):
    db_podcast = podcast_update(db,id,podcast,email,file)
    if db_podcast:
        return {"status": True,"message":"podcast details updated Successfully","records":db_podcast}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "podcast details doesn't exist"})

def delete_podcast(db,podcast_id):
    db_podcast = podcast_delete(db,podcast_id)
    if db_podcast:
        return {"status": True,"message":"podcast details deleted Successfully"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "podcast details doesn't exist"})