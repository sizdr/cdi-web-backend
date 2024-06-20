from fastapi import FastAPI
from .api.routes import users,admin_panel,reviews
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.core import database

models.Base.metadata.create_all(bind=database.engine)
app =  FastAPI()

app.include_router(users.router, tags=["users"])
app.include_router(admin_panel.router, tags=["admin"])
app.include_router(reviews.router)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




