from sqlalchemy.orm import Session
from app import models
from app.schemas import User,UserCreate
from app.core import security


def get_user_by_email(db:Session, email:str) -> User:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db:Session, username: str) -> User:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = security.get_password_hashed(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password,username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db:Session) -> list[User]:
    return db.query(models.User).all()

def authenticate_user_by_username(db:Session, username:str, password:str) -> User:
    user = get_user_by_username(db,username)
    if not user:
        return False
    if not security.verify_password(password,user.hashed_password):
        return False
    return user

def authenticate_user(db:Session, email:str, password:str) -> User:
    user = get_user_by_email(db,email)
    if not user:
        return False
    if not security.verify_password(password,user.hashed_password):
        return False
    return user


