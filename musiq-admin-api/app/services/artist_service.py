from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time
import base64

# from utils.auth_handler import create_access_token
from model.user_model import *
from config.database import *
from model.artist_model import *
from model.admin_user_model import admin_users
from services.admin_user_service import *


def artist_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(artist).filter(artist.is_delete == False).order_by(artist.artist_name).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

def artist_image_check(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete == False,artist.is_image == True).first()

def artist_get_by_id(db,id):
    return db.query(artist).filter(artist.id == id,artist.is_delete==False).first()

def artist_detail(db: Session,artists,email):
    artistname =db.query(artist).filter(artist.artist_name == artists.artist_name,artist.is_delete == False).first()
    a ="AR00"
    if artistname:
        raise HTTPException(status_code=400, detail="artist is already register")
    a ="AR001"
    while db.query(artist).filter(artist.artist_id == a).first():
        a = "AR00" + str(int(a[-1])+1)
    if artists.image:
        s = base64.b64decode(artists.image)
        filename = a+".png"
        file_location = f"{DIRECTORY}/artists/{filename}"
        with open(file_location, "wb+") as f:
            f.write(s)  
        image = True
        # link = f"http://{IPAddr}:2000/public/artists/{filename}"
    else:
        image = False
        # link = null
    temp = admin_get_email(email,db)
    print(email,222222)
    print(temp.id)
    db_user = artist(artist_name = artists.artist_name,
                    artist_id = a,
                    is_image = image,
                    is_delete = False,
                    created_by = temp.id,
                    is_active = 1)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def artist_update(db,user_id,user,email):
    user_temp = artist_get_by_id(db,user_id)
    if user_temp:
        if user.artist_name:
            user_temp.artist_name = user.artist_name
        if user.image:
            s = base64.b64decode(user.image)
            filename = user_temp.artist_id+".png"
            file_location = f"{DIRECTORY}/artists/{filename}"
            with open(file_location, "wb+") as f:
                f.write(s)  
            user_temp.is_image = True
            # user_temp.img_link = f"http://{IPAddr}:2000/public/artists/{filename}"

        temp1 = admin_get_email(email,db)
        user_temp.updated_at = datetime.now()
        user_temp.updated_by = temp1.id
        db.commit()
        # if commit(user_temp,db):
        temp = artist_get_by_id(db,user_id)
        return temp
    return False

def artist_remove_image(db,user_id):
    user_temp =  artist_image_check(db,user_id)
    if user_temp:
        user_temp.is_image = False
        # user_temp.img_link = None
        file = str(user_temp.artist_id)+".png"
        path = f"{DIRECTORY}/artists/{file}"
        os.remove(path)
        db.commit()
        return True
    return False