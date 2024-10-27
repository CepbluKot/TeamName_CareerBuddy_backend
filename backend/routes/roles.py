from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Roles as roles_model, RolesResponseList

from schemas.employees import Roles as roles_schema

from sqlalchemy import select
from sqlalchemy.orm import aliased
from typing import List

from settings import db


api = APIBlueprint("/roles", __name__, url_prefix="/roles", doc_ui=True)
roles_tag = Tag(name="roles", description="roles api")


@api.get(
    "/all_roles",
    tags=[roles_tag],
    responses={HTTPStatus.OK: RolesResponseList},
)
def get_all_roles():
    all_roles = db.session.execute(select(roles_schema)).scalars().all()

    parsed_roles = []

    for role in all_roles:
        parsed = roles_model.from_orm(role)
        parsed_roles.append(parsed.dict())

    return parsed_roles


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
