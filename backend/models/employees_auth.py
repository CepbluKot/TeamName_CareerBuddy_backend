from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema
from models.employees import Employees


class EmployeesAuth(BaseModel):
    id: SkipJsonSchema[int] = Field(None)
    login: str = Field(None)
    password: str = Field(None)
    is_active: SkipJsonSchema[bool] = Field(True)
    
    class Config:
        orm_mode = True


class EmployeeAuthForm(EmployeesAuth):
    name: str = Field("Jonh")
    surname: str = Field("Doe")
    email: str = Field("johndoe@mail.com")
