from requests import Session
from fastapi import Depends,HTTPException
import base64
from datetime import datetime
import os,time

from sqlalchemy import null
# from utils.auth_handler import create_access_token
from model.user_model import *
from model.artist_model import *
from utils.security import verify_password
from config.database import *
from utils.auth_handler import create_access_token,create_refresh_token
from utils.auth_bearer import *

def user_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(users).filter(users.is_delete == False).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

def get_by_id(id,db):
    return db.query(users).filter(users.id == id,users.is_delete==False).first()

def get_email(email,db):
    user = db.query(users).filter(users.email == email,users.is_delete==False).first()
    return user

def username_check(username,db: Session):
    user = db.query(users).filter(users.username == username,users.is_delete==False).first()
    return user

# def access_token_check(token):
#     user = query(token).filter(token.access_token == token).first()
#     return True


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
                        is_delete =data["is_delete"])
    db_token = token(email = data["email"], access_token=access_token,refresh_token = refresh_token)
    
    
   
    db.add(db_user)
    db.add(db_token)
    db.commit()
    db.flush()
    db_user.created_user_by = db_user.id
    db.commit()
    user = db_user
    user.access_token = access_token
    user.refresh_token = refresh_token
    
    print(db_user.id,2222222)
    print(db_user,3333)
    return user

def login_check(user,db):
    temp = get_email(user.email,db)
    if temp:
        tok = db.query(token).filter(token.email == user.email).first()
        if verify_password(user.password,temp.password):
            access_token = create_access_token(user.email)
            access_token_str = access_token.decode('UTF-8')
            # temp.access_token = access_token_str
            refresh_token = create_refresh_token(user.email)
            refresh_token_str = refresh_token.decode('UTF-8')
            # temp.refresh_token = refresh_token_str
            tok.access_token = access_token_str
            tok.refresh_token = refresh_token_str
            db.commit()
            temp1 = get_email(user.email,db)
            temp1.access_token = access_token_str
            temp1.refresh_token = refresh_token_str
            return temp1
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
    return db.query(users).filter(users.id == id,users.is_delete == False,users.is_image == True).first()

# def commit(user,db):
#     temp = db.query(users).filter(users.email == user.name,users.is_delete == 0,users.is_image == 1).first()
#     temp.items = user.items
#     db.commit()
#     return True

def user_update(user_id,user,db,email):
    user_temp = get_by_id(user_id,db)
    temp1 = get_email(email,db)
    if temp1.id == user_id:
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
                file_location = f"{DIRECTORY}/users/{filename}"
                with open(file_location, "wb+") as f:
                    f.write(s)  
                if image_upload(user_id,db):
                    # return {"info": f"file '{filename}' saved at '{file_location}'"}
                    user_temp.is_image = 1
                    # user_temp.img_link = f"http://{IPAddr}:3000/public/users/{filename}"
            user_temp.updated_at = datetime.now()
            user_temp.updated_user_by = temp1.id
            db.commit()
            # if commit(user_temp,db):
            temp = get_by_id(user_id,db)
            return {"status": True,"message":"Updated Successfully","records":temp}
        else:
            raise HTTPException(status_code=404, detail={"success":False,"message":"check your id..user doesn't exist"})
    else:
        raise HTTPException(status_code=403, detail={"success":False,"message":"not authenticated"})

def remove_image(user_id,db):
    user_temp =  image_check(user_id,db)
    if user_temp:
        user_temp.is_image = False
        # user_temp.img_link = None
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
    
# def user_delete(db:Session,user_id):
#     user_temp = db.query(users).filter(users.id == user_id,users.is_delete == False).first()
#     if user_temp:
#         user_temp.is_delete = 1
#         db.commit()
#         return {"success": True,"message":"user deleted"}
#     else:
#         raise HTTPException(status_code=404, detail={"success": False,"message":"user doesn't exist"})

def follower_details(db:Session,user):
    temp = db.query(users).filter(users.register_id == user.user_id,users.is_delete==False).first()
    if temp:
        art = db.query(artist).filter(artist.artist_id == user.artist_id,artist.is_delete==False).first()
        if art:
            num = art.followers
            if num:
                pass
            else:
                num = 0
            if user.follow == False:
                if user.artist_id in temp.preference["artist"]:
                    for i in range(0,len(temp.preference["artist"])):
                        if i < len(temp.preference["artist"]):
                            if temp.preference["artist"][i] == user.artist_id:
                                temp.preference["artist"].pop(i)
                                art.followers = num-1
                            else:
                                pass
                else:
                    raise HTTPException(status_code=400, detail={"success": False,"message":"this user does not folowing this artist"})
                    
            elif user.follow == True:
                if user.artist_id not in temp.preference["artist"]:
                    temp.preference["artist"].append(user.artist_id)
                    art.followers = num + 1
                else:
                    raise HTTPException(status_code=400, detail={"success": False,"message":"this user already folowing this artist"})
        else:
            raise HTTPException(status_code=400, detail={"success": False,"message":"check your artsit id"})
            
    else:
        raise HTTPException(status_code=400, detail={"success": False,"message":"check your user id"})  
    db.commit()
    return {"status": True,"message":"updated successfully"}



        

