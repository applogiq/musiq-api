from app.config.database import  SessionLocal 
import re
from sqlalchemy.orm import Session
from fastapi import HTTPException,Response, status
from datetime import datetime
import os
import shutil
import base64
from typing import List

from app.schema.user_schema import UserresponseSchema
from app.model.artist_model import artist
from app.model.last_song_model import last_songs
from app.model.recent_model import recents
from app.model.user_model import users
from app.model.user_model import token
from app.auth.auth_handler import create_refresh_token,create_token, decodeJWT



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def update_tokens(db: Session, email,access_token, refresh_token):
    tok = db.query(token).filter(token.email == email).first()
    tok.access_token = access_token
    tok.refresh_token =  refresh_token
    db.commit()

def password_check(passwd):  
    SpecialSym =['$', '@', '#', '%','!']
    val = True  
    if len(passwd) < 6:
        val == False
        raise HTTPException(status_code=422, detail='length should be at least 6')    
    if len(passwd) > 20:
        val = False
        raise HTTPException(status_code=422, detail='length should be not be greater than 8')      
    if not any(char.isdigit() for char in passwd):
        val = False
        raise HTTPException(status_code=422, detail='Password should have at least one numeral')      
    if not any(char.isupper() for char in passwd):
        val = False 
        raise HTTPException(status_code=422, detail='Password should have at least one uppercase letter')     
    if not any(char.islower() for char in passwd):
        val = False
        raise HTTPException(status_code=422, detail='Password should have at least one lowercase letter')

    if not any(char in SpecialSym for char in passwd):
        val = False
        raise HTTPException(status_code=422, detail='Password should have at least one of the symbols $@#!%')
    return val

def email_check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def get_user_by_email(db: Session, email, password):
    user = db.query(users).filter(users.email == email,users.is_delete==0).first()
    if user:
        if email == user.email and password == user.password:
                return True
    return False

def register_user(db: Session,user,response):
    if user:
        if (email_check(user.email)) != True:
            raise HTTPException(status_code=422, detail="Invalid Email!!")
        else:
            pass
        if (password_check(user.password)) != True:
            return("Invalid Password !!"),(password_check(user.password))
        else:
            pass
        if user.username:
            user_name =db.query(users).filter(users.username == user.username,users.is_delete == 0).first()
            if user_name:
                raise HTTPException(status_code=400, detail="Username already exist")
            else:
                pass
        else:
            raise HTTPException(status_code=400, detail="Enter your username")
        user_temp = db.query(users).filter(users.email == user.email,users.is_delete==0).first()
        if user_temp:
            raise HTTPException(status_code=400, detail="Email Already Register")
    
        a = 202201
        while db.query(users).filter(users.register_id == a).first():
            a = a+1
        db_user = users(username = user.username,
                        register_id = a,
                        fullname = user.fullname,
                        email = user.email, 
                        password = user.password, 
                        preference = {"artist":[]},
                        is_active = 1, 
                        is_delete = 0, 
                        created_by = 1, 
                        updated_by = 0)
        access_token = create_token(user.email)
        access_token_str = access_token.decode('UTF-8')
        refresh_token = create_refresh_token(user.email)
        refresh_token_str = refresh_token.decode('UTF-8')
        db.add(db_user)
        db.commit()
        db_token = token(email = user.email, access_token=access_token_str, refresh_token = refresh_token_str)
        db.add(db_token)
        db_last_song = last_songs(user_id=a,is_active =1,is_delete=0,created_by=1,updated_by=0)
        db.add(db_last_song)
        db_recent = recents(user_id=a,song_id ={"songs":[]}, is_active =1,is_delete=0,created_by=1,updated_by=0)
        db.add(db_recent)
        db.commit()
        response.status_code = status.HTTP_201_CREATED
        return {'message': "data added","success":True},{"access_token": access_token, "refresh_token": refresh_token}
    else:
        return False


def login_user(db:Session,user):
    if get_user_by_email(db,user.email,user.password):
        access_token = create_token(user.email)
        access_token_str = access_token.decode('UTF-8')
        refresh_token = create_refresh_token(user.email)
        refresh_token_str = refresh_token.decode('UTF-8')
        add =update_tokens(db,user.email,access_token_str,refresh_token_str)
        return {"access_token": access_token, "refresh_token": refresh_token},user
    raise HTTPException(status_code=404, detail={"message": "Wrong login details","success":False})

def follower_details(db:Session,user):
    temp = db.query(users).filter(users.register_id == user.user_id,users.is_delete==0).first()
    if temp:
        art = db.query(artist).filter(artist.artist_id == user.artist_id,artist.is_delete==0).first()
        if art:
            num = art.followers
            if num:
                pass
            else:
                num = 0
            if user.follow == 0:
                if user.artist_id in temp.preference["artist"]:
                    for i in range(0,len(temp.preference["artist"])):
                        if i < len(temp.preference["artist"]):
                            if temp.preference["artist"][i] == user.artist_id:
                                temp.preference["artist"].pop(i)
                                art.followers = num-1
                            else:
                                pass
                else:
                    raise HTTPException(status_code=400, detail="this user does not folowing this artist")
            elif user.follow == 1:
                if user.artist_id not in temp.preference["artist"]:
                    temp.preference["artist"].append(user.artist_id)
                    print("sucess")
                    art.followers = num + 1
                else:
                    raise HTTPException(status_code=400, detail="this user already folowing this artist")
        else:
            raise HTTPException(status_code=400, detail="Check your artsit id")
    else:
        raise HTTPException(status_code=400, detail="Check your user id")
    db.commit()
    return {'message': "Success"}


def token_refresh(db:Session,user):
    refresh_token = user.token
    user = db.query(token).filter(token.refresh_token == refresh_token).first()
    if user:
        new_access_token  = create_token(user.email)
        access_token_str = new_access_token .decode('UTF-8')
        new_refresh_token = create_refresh_token(user.email)
        refresh_token_str = new_refresh_token.decode('UTF-8')
        add =update_tokens(db,user.email,access_token_str,refresh_token_str)
        return {"access_token": new_access_token, "refresh_token": new_refresh_token}
    else:
        raise HTTPException(status_code=404, detail="check your token!!")


def get_user(db: Session, user_id: int):
    user = db.query(users).filter(users.id == user_id,users.is_delete == 0).first()
    if user:
        return user
    else:
        return False
   

def get_users(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(users).filter(users.is_delete == 0).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

def user_update(db: Session,user_id,user):
    user_temp1 = db.query(users).filter(users.id == user_id,users.is_delete == 0).first()
    if user_temp1:
        pass
    else:
        raise HTTPException(status_code=404, detail="user doesn't exist")
    token_temp = db.query(token).filter(token.email == user_temp1.email).first()
    if user.username:
        user_name =db.query(users).filter(users.username == user.username,users.is_delete==0).first()
        if user_name:
            raise HTTPException(status_code=400, detail="Username already exist")
        else:
            user_temp1.username = user.username
    if user.fullname:
        user_temp1.fullname = user.fullname
    if user.email:
        if (email_check(user.email)) == True:
            user_temp = db.query(users).filter(users.email == user.email,users.is_delete==0).first()
            if user_temp:
                raise HTTPException(status_code=400, detail="Email Already Register")
            else:
                user_temp1.email = user.email
                token_temp = db.query(token).filter(token.id == user_id).first()
                token_temp.email = user.email
        else:
            raise HTTPException(status_code=422, detail="Invalid Email!!")
    if user.password:
        if (password_check(user.password)) == True:
            user_temp1.password = user.password
        else:
            return("Invalid Password !!"),(password_check(user.password))

    user_temp1.is_active = 1 
    user_temp1.is_delete = 0
    user_temp1.created_by = 1
    user_temp1.updated_at = datetime.now()
    user_temp1.updated_by = 1

    db.commit()
    db.commit()
    return {'message': "data updated"}

def user_delete(db:Session,user_id):
    user_temp = db.query(users).filter(users.id == user_id,users.is_delete == 0).first()
    if user_temp:
        last_song = db.query(last_songs).filter(last_songs.user_id == user_temp.register_id,last_songs.is_delete == 0).first() 
        recent_song = db.query(recents).filter(recents.user_id == user_temp.register_id,recents.is_delete == 0).first()
        user_temp.is_delete = 1
        last_song.is_delete = 1
        recent_song.is_delete = 1
        db.commit()
        return {"message":"Deleted"}
    else:
        raise HTTPException(status_code=404, detail="user doesn't exist")
    

def upload_new_profile(db: Session,user_id: int,uploaded_file):
    user_temp = db.query(users).filter(users.id == user_id,users.is_delete == 0).first()
    if user_temp: 
        filename1 = str(user_temp.register_id) +"."+"png"
        file_location = f"public/users/{filename1}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(uploaded_file.file, file_object)  

        user_temp.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location}'"}
    else:
        return {'message': "user details doesn't exist"}

def upload_base64_profile(db: Session,user_id: int,img):
    user_temp = db.query(users).filter(users.id == user_id,users.is_delete == 0).first()
    if user_temp:
        s = base64.b64decode(img)
        filename1 = str(user_temp.register_id)+".png"
        file_location = f"public/users/{filename1}"
        with open(file_location, "wb+") as f:
            f.write(s)  

        user_temp.is_image = 1
        db.commit()
        return {"info": f"file '{filename1}' saved at '{file_location}'"}
    else:
        raise HTTPException(status_code=404, detail="user details doesn't exist")



def delete_profile(db: Session,user_id: int):
    user_temp = db.query(users).filter(users.id == user_id,users.is_delete == 0,users.is_image == 1).first()
    if user_temp:
        user_temp.is_image = 0

        file = str(user_temp.register_id)+".png"
        path = f"public/users/{file}"
        os.remove(path)
        db.commit()
        return {'message': "profile image removed"}
    else:
        return {'message': "Check your id"}

def get_profile(db: Session,user_id):
    temp = db.query(users).filter(users.id == user_id,users.is_delete == 0).first()
    if temp:
        user_temp = db.query(users).filter(users.id == user_id,users.is_delete == 0,users.is_image == 1).first()
        if user_temp:
            filename = str(user_temp.register_id)
            link = f"http://127.0.0.1:8000/public/users/{filename}.png"
            return link
        else:
            raise HTTPException(status_code=404, detail="Image doesn't exist for this id")
    else:
        raise HTTPException(status_code=404, detail="check your id")
