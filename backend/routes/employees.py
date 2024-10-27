from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import (
    Employees as employees_model,
    EmployeesResponseList,
    GetEmployeeByIDParams,
    GetAllEmployees,
    EmployeesResponse,
    Departments as departments_model,
    Roles as roles_model,
    GetFilteredEmployees,
)
from schemas.employees import (
    Employees as employees_schema,
    Departments as departments_schema,
    Roles as roles_schema,
)
from sqlalchemy import select
from sqlalchemy.orm import aliased
from typing import List

from settings import db
from services.employees import get_filtered_employees as get_filtered_employees_func


api = APIBlueprint("/employees", __name__, url_prefix="/employees", doc_ui=True)
employees_tag = Tag(name="employees", description="employees api")


@api.get(
    "/all_employees",
    tags=[employees_tag],
    responses={HTTPStatus.OK: EmployeesResponseList},
)
def get_all_employees(query: GetAllEmployees):
    # department_name_alias = aliased(Departments, name='user2')

    all_employees = db.session.execute(
        select(
            employees_schema,
            departments_schema.name.label("department_name"),
            roles_schema.name.label("role_name"),
        )
        .join(
            departments_schema,
            employees_schema.department_id == departments_schema.id,
        )
        .join(roles_schema, employees_schema.role_id == roles_schema.id)
        .limit(query.limit)
        .offset(query.skip)
    ).fetchall()

    parsed_employees = []

    for employee, department_name, role_name in all_employees:
        parsed = EmployeesResponse.from_orm(employee)
        parsed.role_name = role_name
        parsed.department_name = department_name

        parsed_employees.append(parsed.dict())

    return parsed_employees


@api.get(
    "/get_employee", tags=[employees_tag], responses={HTTPStatus.OK: EmployeesResponse}
)
def get_employee(query: GetEmployeeByIDParams):
    employee_data = db.session.execute(
        select(
            employees_schema,
            departments_schema.name.label("department_name"),
            roles_schema.name.label("role_name"),
        )
        .join(
            departments_schema,
            employees_schema.department_id == departments_schema.id,
        )
        .join(roles_schema, employees_schema.role_id == roles_schema.id)
        .where(employees_schema.id == query.id)
    ).fetchone()

    if not employee_data:
        return {
            "code": 1,
            "message": "employee with this id doesnt exist",
        }, HTTPStatus.BAD_REQUEST

    parsed = EmployeesResponse.from_orm(employee_data[0])
    parsed.department_name = employee_data[1]
    parsed.role_name = employee_data[2]

    return parsed.dict()


@api.get(
    "/filtered_employees",
    tags=[employees_tag],
    responses={HTTPStatus.OK: EmployeesResponseList},
)
def get_filtered_employees(query: GetFilteredEmployees):

    parsed_employees = get_filtered_employees_func(
        department_id=query.department_id,
        role_id=query.role_id,
        skip=query.skip,
        limit=query.limit,
    )
    return parsed_employees
