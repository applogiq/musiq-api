from fastapi import HTTPException
import re
from config.database import *
import yagmail,math,random

from services.user_service import *
from utils.auth_handler import *
from utils.security import get_password_hash
from services.admin_user_service import *

###password validator
def password_check(passwd):  
    SpecialSym =['$', '@', '#', '%','!']
    val = True  
    if len(passwd) < 6:
        val == False
        raise HTTPException(status_code=422, detail='Password length should be at least 6')    
    if len(passwd) > 20:
        val = False
        raise HTTPException(status_code=422, detail='Password length should be not be greater than 8')      
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

###email validator
def email_validate(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

###response create new user by admin
def register_user(user,db,email):
    if (email_validate(user.email)) != True:
        raise HTTPException(status_code=422, detail={"message": "Invalid Email!!","success":False})
    if (password_check(user.password)) != True:
        return("Invalid Password !!"),(password_check(user.password))
    if username_check(user.username,db):
        raise HTTPException(status_code=400, detail={"message": "username already exists","success":False})
    if get_email(user.email,db):
        raise HTTPException(status_code=400, detail={"message": "email already exists","success":False})
    access_token = create_access_token(user.email)
    # access_token_str =  access_token.decode('UTF-8')
    refresh_token = create_refresh_token(user.email)
    # refresh_token_str = refresh_token.decode('UTF-8')
    user.password =  get_password_hash(user.password)
    print(user.password)
    dict1 = dict(user)
    temp = admin_get_email(email,db)
    

    s = {"preference" : {"artist":[]},"is_active" : True,"is_delete" : False,"created_by": temp.id}
    data = {**dict1,**s}
    data["access_token"] = access_token
    data["refresh_token"]= refresh_token
    try:
        return {"status": True,"message":"Register Successfully","records":new_register(data,access_token,refresh_token,db)}
    except:
        raise HTTPException(status_code=422, detail={"message": "couldn't register,check your details","success":False})


###login as user
def login_user(user,db):
    if login_check(user,db):
        return {"status": True,"message":"login Successfully","records":login_check(user,db)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't login,check your details","success":False})

###refresh expired access token
def token_refresh(user,db):
    tok_user = get_token_mail(user.token,db)
    if tok_user:
        new_access_token  = create_access_token(tok_user.email)
        # access_token_str = new_access_token .decode('UTF-8')
        new_refresh_token = create_refresh_token(tok_user.email)
        # refresh_token_str = new_refresh_token.decode('UTF-8')
        if update_tokens(tok_user.email,new_access_token,new_refresh_token,db):
            return {"success":True ,"message": "token verified","token":{"access_token": new_access_token, "refresh_token": new_refresh_token}}
    else:
        raise HTTPException(status_code=404, detail={"message": "Check your token!!!","success":False})

###remove profile image of users
def delete_profile(user_id,db):
    if remove_image(user_id,db):
        return {"success":True,'message': "profile image removed"}
    else:
        raise HTTPException(status_code=404, detail={"success":False,'message': "Check your id"})

#############################OTP GENERATE & VERIFY & CHANGE PASSWORD#########################
def generateOTP() :
    '''Generate OTP for forget password of users'''
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP

def email_otp(db,email):
    '''Send OTP to user's email'''
    user = get_email(email.email,db)
    if user:
        s = generateOTP()
        if otp_change(user,s,db):
            user = ('srimathi.k.applogiq@gmail.com')
            password = app_password
            to = 'shajithali.s.applogiq@gmail.com'

            subject = 'Resetting Password'
            content = ['''Password Reset,
                        This OTP valid for next 30 minutes''',s]

            with yagmail.SMTP({user:"MusiQ"}, password) as yag:
                yag.send(to, subject, content)
                print('Sent email successfully')
        return {"success":True,"message":"Sent email successfully"}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your email"})

def verify_otp(db:Session,temp):
    '''verify received OTP'''
    user = get_email(temp.email,db)
    if user:
        if user.otp == temp.otp:
            s = time.time() - user.otp_time
            print(s)
            if s <= 1800:
                return {"success":True,"message":"verified successfully"}
            else:
                raise HTTPException(status_code=400, detail={"success":False,"message":"OTP expired"})
        else:
            raise HTTPException(status_code=400, detail={"success":False,"message":"check your OTP"})  
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your email"})

def password_change(db:Session,temp):
    '''To change password'''
    user = get_email(temp.email,db)
    if user:
        if (password_check(temp.password)) != True:
            return("Invalid Password !!"),(password_check(temp.password))
        temp.password =  get_password_hash(temp.password)
        if update_password(temp.email,temp.password,db):
            return{"success":True,"message":"password changed"}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your email"})

#############################OTP GENERATE & VERIFY & CHANGE PASSWORD#########################

###return response of fetch all user details
def get_all_user(db, skip, limit):
    try:
        users = user_get_all(db, skip, limit)
        if len(users):
            s = len(users)
        else:
            s = 1
        return {"records": users,"totalrecords":s,"success": True}
    except:
        raise HTTPException(status_code=404, detail={"message": "couldn't fetch","success":False})

###return response of get user details
def get_user_by_id(user_id,db):
    db_user = get_by_id(user_id,db)
    if db_user:
        return {"success":True,"message":"user details fetched successfully","records": db_user,"totalrecords" : 1}
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message": "couldn't fetch,check your id"})

###return the response of update user details 
def update_user(user_id,user,db,email):
    db_user = user_update(user_id,user,db,email)
    if db_user:
        return {"status": True,"message":"updated successfully","records":db_user}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "user details doesn't exist"})

###return the response of delete user details 
def delete_user_details(db,user_id):
    db_user = user_delete(db,user_id)
    if db_user:
        return {"success": True,"message":"user details deleted"}
    else:
        raise HTTPException(status_code=404, detail={"success": False,'message': "user details doesn't exist"})