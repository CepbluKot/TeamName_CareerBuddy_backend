from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.json_schema import SkipJsonSchema


class CareerGoals(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    employee_id: SkipJsonSchema[int] = Field(None)
    name: str = Field(None)
    description: str = Field(None)
    start_date: SkipJsonSchema[datetime] = Field(None)
    end_date: SkipJsonSchema[datetime] = Field(None)
    
    class Config:
        orm_mode = True


class GoalCheckpoints(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    career_goal_id: SkipJsonSchema[int] = Field(None)
    description: str = Field(None)
    start_date: SkipJsonSchema[datetime] = Field(None)
    end_date: SkipJsonSchema[datetime] = Field(None)
    
    class Config:
        orm_mode = True
