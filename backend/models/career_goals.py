from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.json_schema import SkipJsonSchema
from typing import List, Any
from pydantic import RootModel


class CareerGoals(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    employee_id: SkipJsonSchema[int] = Field(None)
    name: str = Field(None)
    description: str = Field(None)
    start_date: SkipJsonSchema[datetime] = Field(None)
    end_date: SkipJsonSchema[datetime] = Field(None)

    class Config:
        orm_mode = True
        from_attributes = True


class GoalCheckpoints(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    career_goal_id: SkipJsonSchema[int] = Field(None)
    description: str = Field(None)
    start_date: SkipJsonSchema[datetime] = Field(None)
    end_date: SkipJsonSchema[datetime] = Field(None)

    class Config:
        orm_mode = True
        from_attributes = True


class CareerGoalsWithGoalCheckpoints(CareerGoals):
    goal_checkpoints: List[GoalCheckpoints] = []


class CareerGoalsWithGoalCheckpointsList(RootModel[Any]):
    root: List[CareerGoalsWithGoalCheckpoints]


class GetAllFeedbackFilter(BaseModel):
    skip: int = 0
    limit: int = 100


class GetFilteredFeedbackFilter(BaseModel):
    employee_id: int = -1

    department_id: int = -1
    role_id: int = -1

    start_date: datetime = datetime(year=1970, month=1, day=1, hour=1)
    end_date: datetime = datetime.now()

    skip: int = 0
    limit: int = 100
