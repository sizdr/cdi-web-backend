from fastapi import APIRouter, Depends,HTTPException
from typing import Annotated
from app import crud
from app.schemas import Token, User, UserCreate, User
from app.core import security
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..dependencies import SessionDb,get_current_user,TokenDep


router =  APIRouter(prefix="/api/v1/user")


@router.post("/create_user",response_model= User, status_code=201)
def create_user(user:UserCreate, db: SessionDb):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email alredy registered")
    return crud.create_user(db=db,user=user)


#Endpoint protegido que devuleve la lista de todos los usuarios 
@router.get("/users", response_model= list[User])
def get_users(db:SessionDb,token: TokenDep):
    users = crud.get_users(db)
    return users


#Endpoint para crear token
@router.post("/token")
def login_for_access_token(db:SessionDb, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = crud.authenticate_user_by_username(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="User or password incorrect")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token= access_token, token_type="bearer")


@router.post("/current_user", response_model=User)
async def get_current_user_name(user: Annotated[User,Depends(get_current_user)]):
    return user