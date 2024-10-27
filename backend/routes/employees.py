from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Employees as employees_model, EmployeesResponse, GetEmployeeByIDParams, GetAllEmployees
from schemas.employees import Employees as employees_schema
from sqlalchemy import select
from typing import List

from settings import db


api = APIBlueprint(
    '/employees',
    __name__,
    url_prefix='/employees',
    doc_ui=True
)
employees_tag = Tag(name='employees', description='employees api')


@api.get("/all_employees", tags=[employees_tag], responses={HTTPStatus.OK: EmployeesResponse})
def get_all_employees(query: GetAllEmployees):
    all_employees = db.session.execute(select(employees_schema).offset(query.skip).limit(query.limit)).scalars().all()

    parsed_employees = []
    for employee in all_employees:
        parsed_employees.append(employees_model.from_orm(employee).dict())

    return parsed_employees


@api.get("/get_employee", tags=[employees_tag], responses={HTTPStatus.OK: employees_model})
def get_employee(query: GetEmployeeByIDParams):
    employee_data = db.session.execute(select(employees_schema).where(employees_schema.id == query.id)).scalars().first()

    if not employee_data:
        return {"code": 1, "message": "employee with this id doesnt exist"}, HTTPStatus.BAD_REQUEST

    return employees_model.from_orm(employee_data).dict()
