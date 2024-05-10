from app.core.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(1000), index=True)
    username = Column(String(20),index=True)
    hashed_password = Column(String(1000))