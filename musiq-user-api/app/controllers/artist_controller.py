from fastapi import HTTPException
import re



from services.artist_service import *

def artist_delete_image(db,user_id):
    if artist_remove_image(db,user_id):
        return {"success":True,'message': "artist image removed"}
    else:
        # return {"success":False,'message': "Check your id"}
        raise HTTPException(status_code=404, detail={"success":False,'message': "Check your id"})