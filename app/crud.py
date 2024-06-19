from sqlalchemy.orm import Session
from app import models
from app.schemas import User,UserCreate,UserDB,ReviewCreate,ReviewInDB, UserUpdate
from app.core import security


def get_user_by_email(db:Session, email:str) -> UserDB | None:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db:Session, username: str) -> UserDB | None:
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = security.get_password_hashed(user.password)
    db_user = models.User(email=user.email, password=hashed_password,username=user.username,role_id = user.role.value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def change_password(db:Session, user_db:User, user_in: UserUpdate) -> any:
    new_user_data = user_in.model_dump(exclude_unset=True)
    userDB = user_db.model_dump()
    new_data = {}
    if "password" in new_user_data:
        password = new_user_data["password"]
        hashed_password = security.get_password_hashed(password)
        new_data["password"] = hashed_password
    print("-"*90)
    print(new_data)
    print(new_user_data)
    print("-"*90)
    userDB.copy(update=new_data)
    print(user_db)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db



        
def delete_user(db: Session, id: int) -> any:
    db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return "User delete"

def get_users(db:Session) -> list[User] :
    return db.query(models.User).all()






def create_review(db:Session, user_id:int, review: ReviewCreate) -> ReviewCreate:
    db_review = models.Rating(rating= review.rating, comment= review.comment,user_id = user_id )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review
    
def get_post(db:Session) -> list[ReviewInDB]:
    return db.query(models.Rating).all()







def authenticate_user_by_username(db:Session, username:str, password:str) -> User | None:
    user = get_user_by_username(db,username)
    if not user:
        return False
    if not security.verify_password(password,user.password):
        return False
    return user

def authenticate_user(db:Session, email:str, password:str) -> User | None:
    user = get_user_by_email(db,email)
    if not user:
        return False
    if not security.verify_password(password,user.password):
        return False
    return user
