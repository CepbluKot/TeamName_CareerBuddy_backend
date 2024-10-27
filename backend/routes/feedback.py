from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.feedback import GetFilteredFeedback

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
    "/filtered_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList},
)
def get_filtered_feedback(query: GetFilteredFeedback):
    all_feedback_query = select(feedback_schema)

    employee_alias_for_department_id = aliased(employees_schema)
    employee_alias_for_role_id = aliased(employees_schema)

    if query.to_employee_id and query.to_employee_id != -1:
        all_feedback_query = all_feedback_query.filter(
            feedback_schema.to_employee_id == query.to_employee_id
        )

    if query.from_employee_id and query.from_employee_id != -1:
        all_feedback_query = all_feedback_query.filter(
            feedback_schema.from_employee_id == query.from_employee_id
        )

    if query.department_id and query.department_id != -1:
        all_feedback_query = all_feedback_query.join(
            employee_alias_for_department_id,
            employee_alias_for_department_id.id == feedback_schema.to_employee_id,
        ).filter(employee_alias_for_department_id.department_id == query.department_id)

    if query.role_id and query.role_id != -1:
        all_feedback_query = all_feedback_query.join(
            employee_alias_for_role_id,
            employee_alias_for_role_id.id == feedback_schema.to_employee_id,
        ).filter(employee_alias_for_role_id.role_id == query.role_id)

    if query.limit and query.limit != -1:
        all_feedback_query = all_feedback_query.limit(query.limit)

    else:
        all_feedback_query = all_feedback_query.limit(100)

    if query.skip and query.skip != -1:
        all_feedback_query = all_feedback_query.offset(query.skip)

    all_feedback = db.session.execute(all_feedback_query).scalars().all()

    print("got filtered feedback ", all_feedback)

    parsed_feedback = []

    for feedback in all_feedback:
        parsed = feedback_model.from_orm(feedback)
        parsed_feedback.append(parsed.dict())

    return parsed_feedback


@api.get(
    "/all_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList},
)
def get_all_feedback(query: GetAllFeedback):
    all_feedback = (
        db.session.execute(
            select(feedback_schema).limit(query.limit).offset(query.skip)
        )
        .scalars()
        .all()
    )

    parsed_feedback = []

    for feedback in all_feedback:
        parsed = feedback_model.from_orm(feedback)
        parsed_feedback.append(parsed.dict())

    return parsed_feedback
