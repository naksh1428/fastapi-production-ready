from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String(25))
    description = Column(String(50))
    is_completed = Column(Boolean, default=False)