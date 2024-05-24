from jose import JWTError, jwt
from datetime import timedelta,datetime,timezone
from app.schemas import TokenData
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from crud import get_user_by_email
from typing import Annotated
from sqlalchemy.orm import Session
from app.core import database


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionDb = Annotated[Session, Depends(get_db)]


def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_enconde = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_enconde.update({"exp":expire})
    encoded_jwt = jwt.encode(to_enconde,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


async def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        token_data = TokenData(username=username)
    except JWTError:
        return False
    user = get_user_by_email(SessionDb, token_data.username)
    if user is None:
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPException(status_code=401),
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(SessionDb, token_data.username)
    if user is None:
        raise credentials_exception
    return user