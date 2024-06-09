from app.core.database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date
from sqlalchemy.orm import Relationship

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), index=True)
    username = Column(String(20),index=True)
    password = Column(String(1000))
    role_id = Column(Integer, ForeignKey("role.id"),nullable=False)

    role = Relationship("Role", back_populates="user")
    rating = Relationship("Rating",back_populates="user")




class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    role = Column(String(20), index=True)

    user = Relationship("User",back_populates="role")


class Rating(Base):
    __tablename__ = "rating"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    rating = Column(Integer)
    comment = Column(String(300))

    user = Relationship("User",back_populates="rating")
    