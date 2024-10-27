from pydantic import BaseModel, Field
from typing import List, Any
from pydantic.json_schema import SkipJsonSchema
from pydantic import RootModel


class Employees(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    name: str = Field(None)
    surname: str = Field(None)
    email: str = Field(None)
    department_id: int = Field(None)
    role_id: int = Field(None)
    experience: float = Field(None)
    age: int = Field(None)
    business_travel: str = Field(None)
    daily_rate: int = Field(None)
    distance_from_home: int = Field(None)
    education: int = Field(None)
    education_field: str = Field(None)
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
        from_attributes=True


class EmployeesResponse(RootModel[Any]):
    root: List[Employees]


class GetAllEmployees(BaseModel):
    skip: int = 0
    limit: int = 100

class GetEmployeeByIDParams(BaseModel):
    id: int


class Roles(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    name: str = Field(None)
    admin_page: bool = Field(None)
    feedback_page: bool = Field(None)
    career_goal_page: bool = Field(None)
    
    class Config:
        orm_mode = True


class Departments(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    name: str = Field(None)
    
    class Config:
        orm_mode = True
