from datetime import datetime

from pydantic import BaseModel
class TaskCreate(BaseModel):
     id:int
     title: str
     description: str
     importance: int
     urgency: int
     status: str
     due_date: datetime
     estimated_minutes: int
     credit_reward:int