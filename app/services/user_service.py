from requests import Session
from fastapi import Depends,HTTPException
import base64
from datetime import datetime
import os,time

from sqlalchemy import null

from model.user_model import *
from utils.security import verify_password
from config.database import IPAddr
from utils.auth_handler import create_token,create_refresh_token

def get_by_id(id,db):
    return db.query(users).filter(users.id == id,users.is_delete==0).first()

def get_email(email,db):
    user = db.query(users).filter(users.email == email,users.is_delete==0).first()
    return user

def username_check(username,db: Session):
    user = db.query(users).filter(users.username == username,users.is_delete==0).first()
    return user

def new_register(data,access_token,refresh_token,db:Session):
    a = 202201
    print(data)
    while db.query(users).filter(users.register_id == a).first():
        a = a+1
    data["register_id"] = a
    db_user = users(username = data["username"],
                        register_id = a,
                        fullname = data["fullname"],
                        email = data["email"], 
                        password = data["password"], 
                        preference = data["preference"],
                        is_active = data["is_active"], 
                        is_delete =data["is_delete"], 
                        created_by =data["created_by"], 
                        updated_by =data["updated_by"])
    db_token = token(email = data["email"], access_token=access_token,refresh_token = refresh_token)
    
   
    db.add(db_user)
    db.add(db_token)
    db.commit()
    return True

def login_check(user,db):
    temp = get_email(user.email,db)
    tok = db.query(token).filter(token.email == user.email).first()
    if verify_password(user.password,temp.password):
        temp.access_token = tok.access_token
        temp.refresh_token = tok.refresh_token
        return(temp)
    else:
        return False
   


def get_token_mail(tok,db):
    return db.query(token).filter(token.refresh_token == tok).first()
       
def update_tokens(email,access_token, refresh_token,db:Session):
    tok = db.query(token).filter(token.email == email).first()
    tok.access_token = access_token
    tok.refresh_token =  refresh_token
    db.commit()
    return True

def image_upload(id,db:Session):
    temp = get_by_id(id,db)
    if temp:
        temp.is_image = 1
        db.commit()
    return True

def image_check(id,db:Session):
    return db.query(users).filter(users.id == id,users.is_delete == 0,users.is_image == 1).first()

# def commit(user,db):
#     temp = db.query(users).filter(users.email == user.name,users.is_delete == 0,users.is_image == 1).first()
#     temp.items = user.items
#     db.commit()
#     return True

def user_update(user_id,user,db):
    user_temp = get_by_id(user_id,db)
    if user_temp:
        if user.username:
            if username_check(user.username,db):
                raise HTTPException(status_code=400, detail="Username already exist")
            else:
                user_temp.username = user.username
        if user.fullname:
            user_temp.fullname = user.fullname
        if user.image:
            s = base64.b64decode(user.image)
            filename = str(user_temp.register_id)+".png"
            file_location = f"app/public/users/{filename}"
            with open(file_location, "wb+") as f:
                f.write(s)  
            if image_upload(user_id,db):
                # return {"info": f"file '{filename}' saved at '{file_location}'"}
                user_temp.is_image = 1
                user_temp.img_link = f"http://{IPAddr}:3000/public/users/{filename}"
        user_temp.updated_at = datetime.now()
        user_temp.updated_by = 1 
        db.commit()
        # if commit(user_temp,db):
        temp = get_by_id(user_id,db)
        return {"status": True,"message":"Register Successfully","records":temp}
    else:
        raise HTTPException(status_code=404, detail="user doesn't exist")

def remove_image(user_id,db):
    user_temp =  image_check(user_id,db)
    if user_temp:
        user_temp.is_image = 0
        user_temp.img_link = None
        file = str(user_temp.register_id)+".png"
        path = f"app/public/users/{file}"
        os.remove(path)
        db.commit()
        return True
    else:
        return False

def otp_change(user,s,db):
    user_temp = get_by_id(user.id,db)
    if user_temp:
        user_temp.otp = s
        user_temp.otp_time = time.time()
        db.commit()
    return True

def update_password(email,password,db):
    user_temp = get_email(email,db)
    if user_temp:
        user_temp.password = password
        db.commit()
        return True
    else:
        return False



        

