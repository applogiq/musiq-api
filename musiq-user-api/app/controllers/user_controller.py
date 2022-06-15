from fastapi import HTTPException
import re
import base64
from config.database import *
import yagmail,math,random
# from utils.security import get_password_hash
# from services.user_service import login_check

from services.user_service import *
from utils.auth_handler import *
from utils.security import get_password_hash

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

def email_validate(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def register_user(user,db):
    if (email_validate(user.email)) != True:
        raise HTTPException(status_code=422, detail="Invalid Email!!")
    if (password_check(user.password)) != True:
        return("Invalid Password !!"),(password_check(user.password))
    if username_check(user.username,db):
        raise HTTPException(status_code=400, detail={"message": "username already exists","success":False})
    if get_email(user.email,db):
        raise HTTPException(status_code=400, detail={"message": "email already exists","success":False})
    access_token = create_access_token(user.email)
    access_token_str =  access_token.decode('UTF-8')
    refresh_token = create_refresh_token(user.email)
    refresh_token_str = refresh_token.decode('UTF-8')
    user.password =  get_password_hash(user.password)
    print(user.password)
    dict1 = dict(user)

    s = {"preference" : {"artist":[]},"is_active" : 1,"is_delete" : 0,"created_by" : "user"}
    s1 = {"updated" : 0}
    data = {**dict1,**s}
    data["access_token"] = access_token_str
    data["refresh_token"]= refresh_token_str
    try:
        return {"status": True,"message":"Register Successfully","records": new_register(data,access_token_str,refresh_token_str,db)}
    except:
        raise HTTPException(status_code=422, detail={"message": "couldn't register,check your details","success":False})


def login_user(user,db):
    # if login_check(user,db):
    if login_check(user,db):
        return {"status": True,"message":"login Successfully","records":login_check(user,db)}
    else:
        raise HTTPException(status_code=404, detail={"message": "couldn't login,check your details","success":False})

def token_refresh(user,db):
    tok_user = get_token_mail(user.token,db)
    if tok_user:
        new_access_token  = create_access_token(tok_user.email)
        access_token_str = new_access_token .decode('UTF-8')
        new_refresh_token = create_refresh_token(tok_user.email)
        refresh_token_str = new_refresh_token.decode('UTF-8')
        if update_tokens(tok_user.email,access_token_str,refresh_token_str,db):
            return {"success":True ,"message": "token verified","token":{"access_token": new_access_token, "refresh_token": new_refresh_token}}
    else:
        raise HTTPException(status_code=404, detail={"message": "Check your token!!!","success":False})


# def follower_details(db,user):
#     temp = db.query(users).filter(users.register_id == user.user_id,users.is_delete==0).first()
#     if temp:
#         art = db.query(artist).filter(artist.artist_id == user.artist_id,artist.is_delete==0).first()
#         if art:
#             num = art.followers
#             if num:
#                 pass
#             else:
#                 num = 0
#             if user.follow == 0:
#                 if user.artist_id in temp.preference["artist"]:
#                     for i in range(0,len(temp.preference["artist"])):
#                         if i < len(temp.preference["artist"]):
#                             if temp.preference["artist"][i] == user.artist_id:
#                                 temp.preference["artist"].pop(i)
#                                 art.followers = num-1
#                             else:
#                                 pass
#                 else:
#                     raise HTTPException(status_code=400, detail="this user does not folowing this artist")
#             elif user.follow == 1:
#                 if user.artist_id not in temp.preference["artist"]:
#                     temp.preference["artist"].append(user.artist_id)
#                     print("sucess")
#                     art.followers = num + 1
#                 else:
#                     raise HTTPException(status_code=400, detail="this user already folowing this artist")
#         else:
#             raise HTTPException(status_code=400, detail="Check your artsit id")
#     else:
#         raise HTTPException(status_code=400, detail="Check your user id")
#     db.commit()
#     return {'message': "Success"}

# def upload_base64_profile(db: Session,user_id: int,img):
#     user_temp = get_by_id(user_id,db)
#     if user_temp:
#         s = base64.b64decode(img)
#         filename1 = str(user_temp.register_id)+".png"
#         file_location = f"app/public/users/{filename1}"
#         with open(file_location, "wb+") as f:
#             f.write(s)  
#         if image_upload(user_id,db):
#             return {"info": f"file '{filename1}' saved at '{file_location}'"}
#     else:
#         raise HTTPException(status_code=404, detail="user details doesn't exist")

# def get_profile(db: Session,user_id):
#     temp = get_by_id(user_id,db)
#     if temp:
#         user_temp = image_check(user_id,db)
#         # user_temp = db.query(users).filter(users.id == user_id,users.is_delete == 0,users.is_image == 1).first()
#         if user_temp:
#             filename = str(user_temp.register_id)
#             link = f"http://{IPAddr}:3000/public/users/{filename}.png"
#             return link
#         else:
#             raise HTTPException(status_code=404, detail="Image doesn't exist for this id")
#     else:
#         raise HTTPException(status_code=404, detail="check your id")

def delete_profile(user_id,db):
    if remove_image(user_id,db):
        return {"success":True,'message': "profile image removed"}
    else:
        # return {"success":False,'message': "Check your id"}
        raise HTTPException(status_code=404, detail={"success":False,'message': "Check your id"})



def generateOTP() :
    print(11111)
    digits = "0123456789"
    OTP = ""
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

def email_otp(db,email):
    print(email.email,11111)
    user = get_email(email.email,db)
    if user:
        s = generateOTP()
        if otp_change(user,s,db):
            user = ('srimathi.k.applogiq@gmail.com')
            password = app_password
            to = 'gowtham.r.applogiq@gmail.com'

            subject = 'Resetting Password'
            content = ['''Password Reset,
                        This OTP valid for next 30 minutes''',s]

            with yagmail.SMTP({user:"MusiQ"}, password) as yag:
                yag.send(to, subject, content)
                print('Sent email successfully')
        return {"success":True,"message":"Sent email successfully"}
    else:
        raise HTTPException(status_code=404, detail="Check your email")

def verify_otp(db:Session,temp):
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
    user = get_email(temp.email,db)
    if user:
        if (password_check(user.password)) != True:
            return("Invalid Password !!"),(password_check(user.password))
        user.password =  get_password_hash(user.password)
        if update_password(temp.email,user.password,db):
            return("Password changed")
    else:
        raise HTTPException(status_code=404, detail={"success":False,"message":"check your email"})

# def follow_detail(db,user):
#     if follower_details(db,user):

            