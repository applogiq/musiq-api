from pydantic import BaseModel,Field
from typing import Dict,Optional,List


class UserSchema(BaseModel):
    username : str = Field(...)
    fullname : str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    # preference: Dict[str, list] = None
    class Config:
        schema_extra = {
            "example":{
                "username": "username",
                "fullname" : "first lastname",
                "email": "abcdef@x.com",
                "password": "anypassword"
                
            }
        }
    
def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}

class UserOptional(UserSchema):
    __annotations__ = convert_to_optional(UserSchema)

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

class PostDB(UserSchema):
     id: int

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

class UserResponse(UserSchema):
    id: int = Field(...)
    register_id: int = Field(...)
    preference: dict = Field(...)

    class Config:
        orm_mode = True

class AlluserSchema(BaseModel):
    records: List[UserResponse] = []
    totalrecords: int
    success: bool
    class Config:
        orm_mode = True

class UserresponseSchema(BaseModel):
    records: UserResponse
    totalrecords: int
    success: bool
    class Config:
        orm_mode = True



