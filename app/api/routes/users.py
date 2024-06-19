from fastapi import APIRouter, Depends,HTTPException
from typing import Annotated
from app import crud
from app.schemas import Token, User, UserCreate, UserUpdate
from app.core import security
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..dependencies import SessionDb,get_current_user,CurrentUser


router =  APIRouter(prefix="/api/v1/user")


@router.post("/create_user",response_model= User, status_code=201)
def create_user(user:UserCreate, db: SessionDb):
    db_email = crud.get_user_by_email(db,email=user.email)
    db_username = crud.get_user_by_username(db,username=user.username)
    if db_email:
        raise HTTPException(status_code=400, detail="Email alredy registered")
    elif db_username:
        raise HTTPException(status_code=400, detail="Username alredy registered")
    return crud.create_user(db=db,user=user)


#Endpoint para crear token
@router.post("/login")
async def login_for_access_token(db:SessionDb, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = crud.authenticate_user_by_username(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="User or password incorrect")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token =  security.create_access_token(data={"sub": user.username,"role":user.role_id}, expires_delta=access_token_expires)
    return Token(access_token= access_token, token_type="bearer")

@router.post("/current_user", response_model=User)
async def get_current_user_name(user:CurrentUser):
    return user
