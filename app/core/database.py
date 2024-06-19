from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import CONECTION_URL



SQLALCHEMY_DATABASE_URL = CONECTION_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL,max_overflow=100)

SessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()