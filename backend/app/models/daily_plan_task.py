from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyPlanTask(Base):
    __tablename__ = "daily_plan_tasks"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, nullable=False)
    task_id = Column(Integer, nullable=False)
    priority_rank = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
