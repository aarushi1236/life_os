from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,index=True)
    username = Column(String(100), nullable=False,unique=True)
    email = Column(String(255), nullable=False, unique=True)
    credits = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
