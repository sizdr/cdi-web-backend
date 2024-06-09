from passlib.context import CryptContext
import jwt
from datetime import timedelta,datetime,timezone
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError
from app.schemas import TokenData,Token
from fastapi import HTTPException

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hashed(password: str):
    return pwd_context.hash(password)

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_enconde = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else: 
        expire =  datetime.now(timezone.utc) + timedelta(minutes=15)
    to_enconde.update({"exp":expire})
    encoded_jwt = jwt.encode(to_enconde,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token:Token) -> TokenData:
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
        status_code=401,
        detail="Token has expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    except InvalidTokenError:
        raise HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username : str = payload.get("sub")
    role : int = payload.get("role")
    
    if username is None:
        raise HTTPException(status_code=401)
    token_data = TokenData(username=username, role=role)
    return token_data
