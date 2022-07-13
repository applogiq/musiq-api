from fastapi import status,HTTPException,Request
from fastapi.responses import StreamingResponse
from typing import BinaryIO,Optional

from services.podcast_history_service import *


###response of entering user's podcast history
def create_podcast_history(db: Session,history,email):
    temp = podcast_history_detail(db,history,email)
    if temp:
        return {"success":True,'message': "episode details added","records": temp}
    else:
        return {'message': "check your details","success": False}

###response of get particular user's recent list of songs
def get_podcast_recent(id):
    temp = podcast_recent_user(id)
    if temp:
        return {"success":True,"message": "fetched successfully","records": temp,"totalrecords" : len(temp)}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch"})