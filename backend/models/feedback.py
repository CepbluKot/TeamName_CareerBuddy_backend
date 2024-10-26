from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from pydantic.json_schema import SkipJsonSchema


class Feedback(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    from_employee_id: int = Field(None)
    to_employee_id: int = Field(None)
    from_content: str = Field(None)
    to_content: str = Field(None)
    date_sent: SkipJsonSchema[datetime] = Field(None)
    date_answered: SkipJsonSchema[datetime] = Field(None)
    
    class Config:
        orm_mode = True
