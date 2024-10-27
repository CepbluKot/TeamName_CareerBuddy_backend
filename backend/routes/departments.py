from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Departments as departments_model, DepartmentsResponseList

from schemas.employees import Departments as departments_schema

from sqlalchemy import select
from sqlalchemy.orm import aliased
from typing import List

from settings import db


api = APIBlueprint("/departments", __name__, url_prefix="/departments", doc_ui=True)
departments_tag = Tag(name="departments", description="departments api")


@api.get(
    "/all_departments",
    tags=[departments_tag],
    responses={HTTPStatus.OK: DepartmentsResponseList},
)
def get_all_departments():
    all_departments = db.session.execute(select(departments_schema)).scalars().all()

    parsed_departments = []

    for department in all_departments:
        parsed = departments_model.from_orm(department)
        parsed_departments.append(parsed.dict())

    return parsed_departments


# @api.get(
#     "/get_employee", tags=[feedback_tag], responses={HTTPStatus.OK: EmployeesResponse}
# )
# def get_employee(query: GetEmployeeByIDParams):
#     employee_data = (
#         db.session.execute(
#             select(
#                 employees_schema,
#                 departments_schema.name.label("department_name"),
#                 roles_schema.name.label("role_name"),
#             )
#             .join(
#                 departments_schema,
#                 employees_schema.department_id == departments_schema.id,
#             )
#             .join(roles_schema, employees_schema.role_id == roles_schema.id)
#             .where(employees_schema.id == query.id)
#         )
#         .fetchone()
#     )

#     if not employee_data:
#         return {
#             "code": 1,
#             "message": "employee with this id doesnt exist",
#         }, HTTPStatus.BAD_REQUEST

#     parsed = EmployeesResponse.from_orm(employee_data[0])
#     parsed.department_name = employee_data[1]
#     parsed.role_name = employee_data[2]

#     return parsed.dict()
