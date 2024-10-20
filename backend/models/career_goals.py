from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List
from datetime import datetime


class CareerGoals(BaseModel):
    id: int = Field(None)
    employee_id: UUID = Field(None)
    name: str = Field(None)
    description: str = Field(None)
    start_date: datetime = Field(None)
    end_date: datetime = Field(None)
    
    class Config:
        orm_mode = True


class GoalCheckpoints(BaseModel):
    id: int = Field(None)
    career_goal_id: int = Field(None)
    description: str = Field(None)
    start_date: datetime = Field(None)
    end_date: datetime = Field(None)
    
    class Config:
        orm_mode = True
