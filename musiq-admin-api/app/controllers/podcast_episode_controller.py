from fastapi import HTTPException

from services.podcast_episode_service import *

def create_episode_details(db,episode_name,email,uploaded_file = None):
    temp = episode_details(db,episode_name,email,uploaded_file)
    if temp:
        return {"success":True,'message': "episode details added","records": temp}
    else:
        return {'message': "check your details","success": False}

def get_all_episode(db,limit):
    try:
        users = episode_get_all(db,limit)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"success":True,"message": "fetched successfully","records": users,"totalrecords" : s}
    except:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})

        

def get_episode_by_id(db,id):
    episode = episode_get_by_id(db,id)
    if episode:
        return {"success":True,"message":"details fetched successfully","records": episode,"total_records" : 1}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

def get_episode_by_podcastid(db,id,limit):
    episode = episode_get_by_podcastid(db,id,limit)
    if episode:
        return {"success":True,"message":"details fetched successfully","records": episode,"total_records" : len(episode)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch,check your id","success":False})

# def update_episode(db,id,episode,email,file):
#     db_episode = episode_update(db,id,episode,email,file)
#     if db_episode:
#         return {"status": True,"message":"episode details updated Successfully","records":db_episode}
#     else:
#         raise HTTPException(status_code=404, detail={"success": False,'message': "episode details doesn't exist"})