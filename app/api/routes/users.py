from fastapi import APIRouter, Depends,HTTPException,Form
from typing import Annotated
from sqlalchemy.orm import Session
from app import crud,models
from app.schemas import Token, User, UserCreate, User
from app.core import database, security
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import timedelta

models.Base.metadata.create_all(bind=database.engine)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDb = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router =  APIRouter()

@router.post("/api/v1/create_user",response_model= User)
def create_user(user:UserCreate, db: SessionDb):
    db_user = crud.get_user_by_email(db,email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email alredy registered")
    return crud.create_user(db=db,user=user)

@router.get("/api/v1/users", response_model= list[User])
def get_users(db:SessionDb,token: Annotated[str,Depends(oauth2_scheme)]):
    users = crud.get_users(db)
    return users

@router.post("/token")
def login_for_access_token(db:SessionDb, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = crud.authenticate_user(db,form_data.username, form_data.password)
    print(form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="User or password incorrect")

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token= access_token, token_type="bearer")

@router.post("/api/v1//login", response_model=User)
def login(user_login: User,db: SessionDb):
    user = crud.authenticate_user(db,user_login.email,user_login.password)
    if not user:
        raise HTTPException(status_code=401,detail="El usuario o la contraseña son incorrectos")
    return user
