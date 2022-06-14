from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64

from sqlalchemy import null
# from utils.auth_handler import create_access_token
from model.user_model import *
from config.database import *
from model.artist_model import *

def artist_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(artist).filter(artist.is_delete == 0).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

def artist_image_check(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete == 0,artist.is_image == 1).first()

def artist_get_by_id(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete==0).first()

def artist_detail(db: Session,artists):
    artistname =db.query(artist).filter(artist.name == artists.name,artist.is_delete == 0).first()
    a ="AR00"
    if artistname:
        raise HTTPException(status_code=400, detail="Artist is already register")
    a ="AR001"
    while db.query(artist).filter(artist.artist_id == a).first():
        a = "AR00" + str(int(a[-1])+1)
    if artists.image:
        s = base64.b64decode(artists.image)
        filename = a+".png"
        file_location = f"{DIRECTORY}/artists/{filename}"
        with open(file_location, "wb+") as f:
            f.write(s)  
        image = 1
        # link = f"http://{IPAddr}:2000/public/artists/{filename}"
    else:
        image = 0
        # link = null

    db_user = artist(name = artists.name,
                    artist_id = a,
                    is_image = image,
                    is_delete = 0,
                    created_by = 1,
                    updated_by = 0,
                    is_active = 1)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"success": True,"message":"data added","records":{db_user}}

def artist_update(db,user_id,user):
    user_temp = artist_get_by_id(db,user_id)
    if user_temp:
        if user.name:
            user_temp.name = user.name
        if user.image:
            s = base64.b64decode(user.image)
            filename = user_temp.artist_id+".png"
            file_location = f"{DIRECTORY}/artists/{filename}"
            with open(file_location, "wb+") as f:
                f.write(s)  
            user_temp.is_image = 1
            # user_temp.img_link = f"http://{IPAddr}:2000/public/artists/{filename}"
       
        user_temp.updated_at = datetime.now()
        user_temp.updated_by = 1 
        db.commit()
        # if commit(user_temp,db):
        temp = artist_get_by_id(db,user_id)
        return {"status": True,"message":"updated successfully","records":temp}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your id..user doesn't exist"})

def artist_remove_image(db,user_id):
    user_temp =  artist_image_check(db,user_id)
    if user_temp:
        user_temp.is_image = 0
        # user_temp.img_link = None
        file = str(user_temp.artist_id)+".png"
        path = f"{DIRECTORY}/artists/{file}"
        os.remove(path)
        db.commit()
        return True
    else:
        return False