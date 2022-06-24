from fastapi import HTTPException
import re

from services.user_service import *
from services.admin_user_service import *
from utils.auth_handler import *
from utils.security import get_password_hash
from config.database import *
from controllers.user_controller import *


def register_admin(user,db):
    if (email_validate(user.email)) != True:
        raise HTTPException(status_code=422, detail="Invalid Email!!")
    if (password_check(user.password)) != True:
        return("Invalid Password !!"),(password_check(user.password))
    if admin_get_email(user.email,db):
        return("email already exists")
    access_token = create_access_token(user.email)
    access_token_str =  access_token.decode('UTF-8')
    refresh_token = create_refresh_token(user.email)
    refresh_token_str = refresh_token.decode('UTF-8')
    user.password =  get_password_hash(user.password)
    print(user.password)
    dict1 = dict(user)

    s = {"is_active" : True,"is_delete" : False}
    data = {**dict1,**s}
    data["access_token"] = access_token_str
    data["refresh_token"]= refresh_token_str
    if new_admin_register(data,access_token_str,refresh_token_str,db):
        return {"status": True,"message":"Register Successfully","records":data}
    else:
        raise HTTPException(status_code=422, detail={"message": "couldn't register,check your details","success":False})

def login_admin(user,db):
    if admin_login_check(user,db):
        return {"status": True,"message":"login Successfully","records":admin_login_check(user,db)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't login,check your details","success":False})

def admin_token_refresh(user,db):
    tok_user = admin_get_token_mail(user.token,db)
    if tok_user:
        new_access_token  = create_access_token(tok_user.email)
        access_token_str = new_access_token .decode('UTF-8')
        new_refresh_token = create_refresh_token(tok_user.email)
        refresh_token_str = new_refresh_token.decode('UTF-8')
        if admin_update_tokens(tok_user.email,access_token_str,refresh_token_str,db):
            return {"success":True ,"message": "token verified","token":{"access_token": new_access_token, "refresh_token": new_refresh_token}}
    else:
        raise HTTPException(status_code=404, detail={"message": "Check your token!!!","success":False})


def get_all_admin_details(db, skip, limit):
    try:
        users = admin_get_all(db, skip, limit)
        return {"success": True,"message":"fetched Successfully","records": users,"totalrecords":len(users)}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

def get_admin_by_id(admin_id,db):
    admin = admin_get_by_id(admin_id,db)
    if admin:
        return {"success": True,"message":"fetched Successfully","records":admin,"total_records":1}
    else:
        raise HTTPException(status_code=422, detail={"message": "Couldn't fetch...Check your id","success":False})

def update_admin(admin_id,admin,db,email):
    db_admin =  admin_update(admin_id,admin,db,email)
    if db_admin:
        return  {"status": True,"message":"updated successfully","records":db_admin}
    else:
        raise HTTPException(status_code=404, detail={"success":False,'message':"admin details doesn't exist"})

def delete_admin_details(db,admin_id):
    db_admin = admin_delete(db,admin_id)
    if db_admin:
        return {"success": True,"message":"admin details deleted"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "admin details doesn't exist"})