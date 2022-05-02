# from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship

from modules.api_modules.db_api.database import Base

class Rules(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String, )
    value = Column(Float, )
    TresholdType = Column(String,)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="rules")

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    chat_id = Column(Integer, )
    rules = relationship("Rules", back_populates="owner")