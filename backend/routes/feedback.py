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
)

from models.feedback import Feedback as feedback_model, FeedbackList, GetAllFeedback

from schemas.feedback import Feedback as feedback_schema
from schemas.employees import (
    Employees as employees_schema,
    Departments as departments_schema,
    Roles as roles_schema,
)
from sqlalchemy import select
from sqlalchemy.orm import aliased
from typing import List

from settings import db


api = APIBlueprint("/feedback", __name__, url_prefix="/feedback", doc_ui=True)
feedback_tag = Tag(name="feedback", description="employees api")


@api.get(
    "/all_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList},
)
def get_all_employees(query: GetAllFeedback):
    all_feedback = (
        db.session.execute(
            select(
                feedback_schema
            )
            .limit(query.limit)
            .offset(query.skip)
        )
        .scalars().all()
    )

    parsed_feedback = []

    for feedback in all_feedback:
        parsed = feedback_model.from_orm(feedback)
        parsed_feedback.append(parsed.dict())
    
    return parsed_feedback


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
