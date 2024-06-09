from pydantic import BaseModel , EmailStr
from enum import Enum

class Role(int,Enum):
    Free = 1
    Premiun = 2
    Admin = 3



class UserBase(BaseModel):
    email : EmailStr
    username: str

class UserCreate(UserBase):
    password : str
    role: Role

class User(UserBase):
    id : int
    role_id: int
    class Config:
        from_attributes = True

class UserDB(User):
    password : int




class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username: str
    role: int