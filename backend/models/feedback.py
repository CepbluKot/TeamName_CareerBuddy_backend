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
    template_id: int = Field(None)
    answer_content: str = ""
    date_sent: SkipJsonSchema[datetime] = Field(None)
    date_answered: SkipJsonSchema[datetime] = Field(None)

    class Config:
        orm_mode = True
        from_attributes = True


class FeedbackTemplate(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    name: str = Field(None)
    content: str = Field(None)

    class Config:
        orm_mode = True
        from_attributes = True


class FeedbackList(RootModel[Any]):
    root: List[Feedback]


class FeedbackTemplateList(RootModel[Any]):
    root: List[FeedbackTemplate]


class GetAllFeedback(BaseModel):
    skip: int = 0
    limit: int = 100


class GetUsersFeedbackTemplate(BaseModel):
    id: int = 0
    skip: int = 0
    limit: int = 100


class GetFilteredFeedback(BaseModel):
    to_employee_id: int = -1
    from_employee_id: int = -1
    department_id: int = -1
    role_id: int = -1
    skip: int = -1
    limit: int = -1


class CreateFeedback(BaseModel):
    user_id: int
    department_id: int = -1
    role_id: int = -1
    feedback_form_template_id: int


class CreateFeedbackAnswer(BaseModel):
    feedback_id: int
    answer_content: int
    date_answered: datetime = Field(default_factory=datetime.now)
