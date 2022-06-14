from pydantic import BaseModel,Field
from typing import Dict,Optional,List

class UserSchema(BaseModel):
    username : str = Field(...)
    fullname : str = Field(...)
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "username": "username",
                "fullname" : "first lastname",
                "email": "abcdef@x.com",
                "password": "anypassword"
                
            }
        }

class UserLoginSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "email": "abcdef@x.com",
                "password": "givenpassword"
            }
        }

class Refresh_token(BaseModel):
    token: str = Field(...)
    class Config:
        schema_extra = {
            "example":{
                "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWJjZGVmNzY4QHguY29tIiwiZXhwaXJlcyI6MTY1MjE4NTAyNC45NjQ5ODY2fQ.KS_Eeyy3ugQRcIJrG1bSoQGQXQl31eOquy0oI-FP_pE"
            }
        }

class FollowerSchema(BaseModel):
    user_id : int
    artist_id: str
    follow : int
    class Config:
        schema_extra = {
            "example":{
                "user_id": 202201,
                "artist_id": "AR00ANI",
                "follow": 0
            }
        }

class UserOptional(BaseModel):
    username : Optional[str] = Field(...)
    fullname : Optional[str] = Field(...)
    image: Optional[str] = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "username": "username",
                "fullname" : "first lastname",
                "image" : "dkfnsndfisdfhdfn"
            }
        }

class OtpSend(BaseModel):
    email : str
    class Config:
        orm_mode = True
   


class OtpVerify(OtpSend):
    otp : str
    class Config:
        orm_mode = True

class PasswordSchema(OtpSend):
    password : str
    class Config:
        orm_mode = True