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


def get_filtered_employees(
    department_id: int = -1, role_id: int = -1, skip: int = 0, limit: int = 100
) -> List[EmployeesResponse]:

    filtered_employees_query = (
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
    )

    if department_id and department_id != -1:
        filtered_employees_query = filtered_employees_query.filter(
            employees_schema.department_id == department_id
        )

    if role_id and role_id != -1:
        filtered_employees_query = filtered_employees_query.filter(
            employees_schema.role_id == role_id
        )

    if limit and limit != -1:
        filtered_employees_query = filtered_employees_query.limit(limit)

    else:
        filtered_employees_query = filtered_employees_query.limit(100)

    if skip and skip != -1:
        filtered_employees_query = filtered_employees_query.offset(skip)

    all_employees = db.session.execute(filtered_employees_query).fetchall()

    parsed_employees = []

    for employee, department_name, role_name in all_employees:
        parsed = EmployeesResponse.from_orm(employee)
        parsed.role_name = role_name
        parsed.department_name = department_name

        parsed_employees.append(parsed.dict())

    return parsed_employees
