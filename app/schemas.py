from pydantic import BaseModel , EmailStr, Field
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

class UserUpdate(BaseModel):
    password: str | None = None
    username: str | None = None




class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username: str
    role: int


class ReviewCreate(BaseModel):
    rating: int
    comment: str | None = None

class ReviewInDB(ReviewCreate):
    id: int
    user_id: int



