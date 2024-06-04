from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from ..crud import get_user_by_username
from typing import Annotated
from sqlalchemy.orm import Session
from app.core import database
from app.core.security import decode_token


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDb = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str,Depends(oauth2_scheme)]


async def get_current_user(session: SessionDb, token: TokenDep):
    token_data = await decode_token(token=token)
    user = get_user_by_username(session, username=token_data.username)
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user

async def verify_token(token:TokenDep):
    try:
        token_data = decode_token(token=token)
    except :
        raise HTTPException(status_code=401)
    return token_data
