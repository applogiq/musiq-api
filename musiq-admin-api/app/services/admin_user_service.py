from requests import Session
from fastapi import Depends,HTTPException
from datetime import datetime
import os,time

from sqlalchemy import null
# from utils.auth_handler import create_access_token
from model.user_model import *
from utils.security import verify_password
from config.database import *
from utils.auth_handler import create_access_token,create_refresh_token
from model.admin_user_model import *

def admin_get_all(db: Session, skip: int = 0, limit: int = 100):
    user = db.query(admin_users).filter(admin_users.is_delete == False).offset(skip).limit(limit).all()
    if user:
        return user
    else:
        return False

def admin_get_by_id(id,db):
    return db.query(admin_users).filter(admin_users.id == id,admin_users.is_delete==False).first()

def admin_get_email(email,db):
    user = db.query(admin_users).filter(admin_users.email == email,admin_users.is_delete==False).first()
    return user



def new_admin_register(data,access_token,refresh_token,db:Session):
    db_user = admin_users(name = data["name"],
                    email = data["email"], 
                    password = data["password"], 
                    is_active = data["is_active"], 
                    is_delete =data["is_delete"])
    db_token = admin_token(email = data["email"], access_token=access_token,refresh_token = refresh_token)
    
   
    db.add(db_user)
    db.add(db_token)
    db.commit()
    db.flush()
    db_user.created_by = db_user.id
    db.commit()
    return True

def admin_login_check(user,db):
    temp =admin_get_email(user.email,db)
    if temp:
        tok = db.query(admin_token).filter(admin_token.email == user.email).first()
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
            temp1 = admin_get_email(user.email,db)
            temp1.access_token = access_token_str
            temp1.refresh_token = refresh_token_str
            return temp1
    else:
        return False
   

def admin_get_token_mail(tok,db):
    return db.query(admin_token).filter(admin_token.refresh_token == tok).first()
       
def admin_update_tokens(email,access_token, refresh_token,db:Session):
    tok = db.query(admin_token).filter(admin_token.email == email).first()
    tok.email = email
    tok.access_token = access_token
    tok.refresh_token =  refresh_token
    db.commit()
    return True

def admin_user_update(user_id,user,db,email):
    user_temp = admin_get_by_id(user_id,db)
    if user_temp:
        if user.name:
            user_temp.name = user.name
        if user.email:
            user_temp.email = user.email
        if user.password:
            user_temp.password = user.password
        user_temp.updated_at = datetime.now()
        temp = admin_get_email(email,db)
        user_temp.updated_by = temp.id
        db.commit()
        # if commit(user_temp,db):
        temp = admin_get_by_id(user_id,db)
        return {"status": True,"message":"Register Successfully","records":temp}
    else:
        raise HTTPException(status_code=404, detail="user doesn't exist")

def admin_delete(db:Session,user_id):
    user_temp = admin_get_by_id(user_id,db)
    if user_temp:
        user_temp.is_delete = True
        db.commit()
        return {"success": True,"message":"user deleted"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,"message":"user doesn't exist"})