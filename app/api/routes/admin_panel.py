from fastapi import APIRouter, Depends
from app import crud
from ..dependencies import SessionDb,admin_authorization
from app.schemas import User,ReviewInDB


router = APIRouter(
    dependencies=[Depends(admin_authorization)],
    prefix="/admin"
)

#Endpoint protegido que devuleve la lista de todos los usuarios 
@router.get("/users", response_model= list[User])
def get_users(db:SessionDb):
    users = crud.get_users(db)
    return users

#Endpoint protegido que requiere permisos de administrador para retornar un usuario de acuerdo a su nombre de usuiario
@router.get("/get_user/{username}", response_model= User)
def get_user(db:SessionDb, username:str):
    user = crud.get_user_by_username(db,username)
    return user

#Endpoint que elimina a un usuario por su id
@router.delete("/delete_user/{id}")
def delete_user(db:SessionDb,id:int) -> any:
    return crud.delete_user(db,id)

#Endpoint que retorna todos las calificaciones hechas
@router.get("/get_posts", response_model= list[ReviewInDB])
def get_user(db:SessionDb):
    return crud.get_post(db)

