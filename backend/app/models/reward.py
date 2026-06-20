from sqlalchemy import Column, Integer, String
from ..database.base import Base

class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    credit_cost = Column(Integer)
    reward_type = Column(String)
    description = Column(String)  # e.g., "item", "experience", etc.