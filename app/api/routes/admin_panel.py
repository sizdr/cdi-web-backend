from fastapi import APIRouter, Depends,HTTPException
from app import crud
from ..dependencies import SessionDb,admin_authorization
from app.schemas import User,UserCreate,UserDB


router = APIRouter()

#Endpoint protegido que devuleve la lista de todos los usuarios 
@router.get("/users", response_model= list[User], dependencies=[Depends(admin_authorization)])
def get_users(db:SessionDb):
    users = crud.get_users(db)
    return users

@router.get("/get_user/{username}", response_model= User, dependencies=[Depends(admin_authorization)])
def get_user(db:SessionDb, username:str):
    user = crud.get_user_by_username(db,username)
    return user

@router.delete("/delete_user{id}")
def delete_user():
    pass

@router.put("/edit_user")
def edit_user():
    pass

@router.post("/create_user",response_model= User, status_code=201)
def create_user(user:UserCreate, db: SessionDb):
    db_email = crud.get_user_by_email(db,email=user.email)
    db_username = crud.get_user_by_username(db,username=user.username)
    if db_email:
        raise HTTPException(status_code=400, detail="Email alredy registered")
    elif db_username:
        raise HTTPException(status_code=400, detail="Username alredy registered")
    return crud.create_user(db=db,user=user)
