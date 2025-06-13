# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    profile = relationship("Profile", uselist=False, back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    username = Column(String, index=True)
    description = Column(String)
    position = Column(String)
    avatar_url = Column(String)
    user = relationship("User", back_populates="profile")
