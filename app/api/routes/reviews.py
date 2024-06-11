from fastapi import APIRouter
from app import crud
from ..dependencies import SessionDb,CurrentUser
from app.schemas import ReviewCreate


router = APIRouter(
    prefix="/review"
)

#Endpoint protegido que permite crear una reseña para la pagina
@router.post("/post_review", response_model= ReviewCreate)
def post_review(db:SessionDb,user:CurrentUser, review:ReviewCreate):
    print(user)
    post = crud.create_review(db,user_id=user.id,review=review)
    return post