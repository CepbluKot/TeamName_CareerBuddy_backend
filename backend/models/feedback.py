from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from pydantic.json_schema import SkipJsonSchema
from typing import List, Any
from pydantic import RootModel


class Feedback(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    from_employee_id: int = Field(None)
    to_employee_id: int = Field(None)
    answer_content: str = ""
    date_sent: SkipJsonSchema[datetime] = Field(None)
    date_answered: SkipJsonSchema[datetime] = Field(None)
    
    class Config:
        orm_mode = True
        from_attributes = True


class FeedbackList(RootModel[Any]):
    root: List[Feedback]


class GetAllFeedback(BaseModel):
    skip: int = 0
    limit: int = 100
