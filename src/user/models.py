from  sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    username = Column(String(25), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(30))