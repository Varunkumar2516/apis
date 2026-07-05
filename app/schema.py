from pydantic import BaseModel , EmailStr , Field,ConfigDict
import re
from datetime import datetime
from typing import Optional,Literal 
from sqlalchemy.dialects.postgresql import UUID

password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[a-zA-Z\d!@#$%^&*_=+]{8,64}$')
class UserCreate(BaseModel):
    name:str
    email:EmailStr
    password:str = Field(...,
                         pattern=password_regex,
                         description='Password Must Contain 1 digit 1 uppercase 1 lowercase and 1 Special Symbol')
 
class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr 
    
    model_config = ConfigDict(from_attributes=True)
 
class PostBase(BaseModel):
    title:str
    content:str
    published : bool = True


class CreatePost(PostBase):
    pass
   
class UpdatePost(PostBase):
    published : bool
    updated_at :Optional[datetime] = None
  

class PostResponse(PostBase):
    user_id:int
    id:int 
    created_at : datetime
    updated_at : datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email:EmailStr
    password : str 


class Token(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str ='bearer'


class TokenData(BaseModel):
    user_id : int 
    type : Literal["access", "refresh","email-verify",'reset-password']
    exp : datetime
    iat : datetime 
    jti : str

class CurrentUser(BaseModel):
    id:int 
    name:str

class refreshToken(BaseModel):
    refresh_token : str

simple_password_regex = re.compile(r'^[a-zA-Z\d]{8,64}$')
class PasswordChange(BaseModel):
    old_password : str
    new_password : str = Field(...,
                         pattern=simple_password_regex,
                         description='Password Must Contain 1 digit 1 uppercase 1 lowercase and 1 Special Symbol')
 
    confirm_password : str = Field(...,
                         pattern=simple_password_regex,
                         description='Password Must Contain 1 digit 1 uppercase 1 lowercase and 1 Special Symbol')
 

class PasswordForget(BaseModel):
    email : EmailStr


class PasswordReset(BaseModel):
    token :str
    new_password : str = Field(...,
                         pattern=simple_password_regex,
                         description='Password Must Contain 1 digit 1 uppercase 1 lowercase and 1 Special Symbol')
 
    confirm_password : str = Field(...,
                         pattern=simple_password_regex,
                         description='Password Must Contain 1 digit 1 uppercase 1 lowercase and 1 Special Symbol')
 