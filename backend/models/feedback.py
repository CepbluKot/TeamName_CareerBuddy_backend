from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List
from datetime import datetime


class Feedback(BaseModel):
    id: int = Field(None)
    from_employee_id: UUID = Field(None)
    to_employee_id: UUID = Field(None)
    from_content: str = Field(None)
    to_content: str = Field(None)
    date_sent: datetime = Field(None)
    date_answered: datetime = Field(None)
    
    class Config:
        orm_mode = True
