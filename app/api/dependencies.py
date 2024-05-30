import jwt
from jwt.exceptions import InvalidTokenError
from app.schemas import TokenData,Token
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from ..crud import get_user_by_username
from typing import Annotated
from sqlalchemy.orm import Session
from app.core import database


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDb = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str,Depends(oauth2_scheme)]

def decode_token(token:Token) -> TokenData:
    payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
    username :str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=401)
    token_data = TokenData(username=username)
    return token_data

async def get_current_user(session: SessionDb, token: TokenDep):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = decode_token(token=token)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_username(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def verify_token(token:TokenDep):
    try:
        token_data = decode_token(token=token)
        return token_data
    except InvalidTokenError:
        raise HTTPException(status_code=401)
