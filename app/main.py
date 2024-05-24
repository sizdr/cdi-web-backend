from fastapi import FastAPI
from .api.routes import users
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.core import database

models.Base.metadata.create_all(bind=database.engine)
app =  FastAPI()

app.include_router(users.router, tags=["users"])

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5500/CDI-Web/CDI%20WEB%20Rep/HTML/signin.html?",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




