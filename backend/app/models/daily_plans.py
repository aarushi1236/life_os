from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DailyPlan(Base):
    __tablename__ = "daily_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    plan_date = Column(DateTime(timezone=True), nullable=False)
    generated_at = Column(DateTime(timezone=False), server_default=func.now())


    