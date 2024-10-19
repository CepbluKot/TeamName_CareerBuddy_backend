from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List


class Employees(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    name: str = Field(None)
    surname: str = Field(None)
    email: str = Field(None)
    department: str = Field(None)
    role_id: int = Field(None)
    experience: float = Field(None)
    age: int = Field(None)
    business_travel: List[str] = Field(None)
    daily_rate: int = Field(None)
    distance_from_home: int = Field(None)
    education: int = Field(None)
    education_field: List[str] = Field(None)
    employee_number: int = Field(None)
    relationship_satisfaction: int = Field(None)
    standard_hours: int = Field(None)
    stock_option_level: int = Field(None)
    total_working_years: int = Field(None)
    training_time_last_year: int = Field(None)
    work_life_balance: int = Field(None)
    years_at_company: int = Field(None)
    years_in_current_role: int = Field(None)
    years_since_last_promotion: int = Field(None)
    years_with_cur_manager: int = Field(None)

    class Config:
        orm_mode = True
