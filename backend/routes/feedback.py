import logging
from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.feedback import GetFilteredFeedback

from models.feedback import Feedback as feedback_model, FeedbackList, GetAllFeedback, CreateFeedback, CreateFeedbackAnswer, FeedbackTemplateList, FeedbackTemplate as feedback_template_model, GetUsersFeedbackTemplate

from schemas.feedback import Feedback as feedback_schema, FeedbackTemplates as feedback_template_schema
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
from datetime import datetime


api = APIBlueprint("/feedback", __name__, url_prefix="/feedback", doc_ui=True)
feedback_tag = Tag(name="feedback", description="employees api")


@api.get(
    "/filtered_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList},
)
def get_filtered_feedback(query: GetFilteredFeedback):
    filtered_feedback_query = select(feedback_schema)

    employee_alias_for_department_id = aliased(employees_schema)
    employee_alias_for_role_id = aliased(employees_schema)

    if query.to_employee_id and query.to_employee_id != -1:
        filtered_feedback_query = filtered_feedback_query.filter(
            feedback_schema.to_employee_id == query.to_employee_id
        )

    if query.from_employee_id and query.from_employee_id != -1:
        filtered_feedback_query = filtered_feedback_query.filter(
            feedback_schema.from_employee_id == query.from_employee_id
        )

    if query.department_id and query.department_id != -1:
        filtered_feedback_query = filtered_feedback_query.join(
            employee_alias_for_department_id,
            employee_alias_for_department_id.id == feedback_schema.to_employee_id,
        ).filter(employee_alias_for_department_id.department_id == query.department_id)

    if query.role_id and query.role_id != -1:
        filtered_feedback_query = filtered_feedback_query.join(
            employee_alias_for_role_id,
            employee_alias_for_role_id.id == feedback_schema.to_employee_id,
        ).filter(employee_alias_for_role_id.role_id == query.role_id)

    if query.limit and query.limit != -1:
        filtered_feedback_query = filtered_feedback_query.limit(query.limit)

    else:
        filtered_feedback_query = filtered_feedback_query.limit(100)

    if query.skip and query.skip != -1:
        filtered_feedback_query = filtered_feedback_query.offset(query.skip)

    all_feedback = db.session.execute(filtered_feedback_query).scalars().all()

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


@api.get(
    "/all_feedback_templates",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackTemplateList},
)
def get_all_feedback_templates(query: GetAllFeedback):
    all_feedback = (
        db.session.execute(
            select(feedback_template_schema).limit(query.limit).offset(query.skip)
        )
        .scalars()
        .all()
    )

    parsed_feedback_templates = []

    for feedback in all_feedback:
        parsed = feedback_template_model.from_orm(feedback)
        parsed_feedback_templates.append(parsed.dict())

    return parsed_feedback_templates


@api.get(
    "/get_employees_feedback_template",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackTemplateList},
)
def get_users_feedback_template(query: GetUsersFeedbackTemplate):
    all_feedback = (
        db.session.execute(
            select(feedback_template_schema).limit(query.limit).offset(query.skip).where(feedback_template_schema.created_by_employee_id == 1)
        )
        .scalars()
        .all()
    )

    parsed_feedback_templates = []

    for feedback in all_feedback:
        parsed = feedback_template_model.from_orm(feedback)
        parsed_feedback_templates.append(parsed.dict())

    return parsed_feedback_templates


@api.post(
    "/create_feedback_template",
    tags=[feedback_tag]
)
def create_feedback_template(body: feedback_template_model):


    new_feedback_template = feedback_template_schema(name=body.name, content=body.content, created_by_employee_id=123)
    db.session.add(new_feedback_template)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.error("error occupied during creation of new feedback template")

    return {"code": 0, "message": "ok"}, HTTPStatus.OK


@api.post(
    "/create_feedback",
    tags=[feedback_tag],
)
def create_feedback(body: CreateFeedback):
    does_template_exists = (
        db.session.execute(
            select(feedback_template_schema).where(feedback_template_schema.id == body.feedback_form_template_id)
        )
        .scalar()
    )

    if not does_template_exists:
        return {"code": 1, "message": "feedback template doesnt exist"}, HTTPStatus.BAD_REQUEST

    filtered_employees = get_filtered_employees_func(department_id=body.department_id, role_id=body.role_id)
    

    for employee in filtered_employees:
        new_feedback = feedback_schema(from_employee_id=1, to_employee_id=employee.id,date_sent=datetime.now(), template_id=body.feedback_form_template_id)
        db.session.add(new_feedback)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.error("error occupied during creation of new feedback")

    return {"code": 0, "message": "ok"}, HTTPStatus.OK



@api.post(
    "/create_feedback_answer",
    tags=[feedback_tag],
)
def create_feedback_answer(body: CreateFeedbackAnswer):
    feedback = (
        db.session.execute(
            select(feedback_schema).where(feedback_schema.id == body.feedback_id)
        )
        .scalar()
    )

    if not feedback:
        return {"code": 1, "message": "feedback doesnt exist"}, HTTPStatus.BAD_REQUEST

    feedback_answer = feedback_model.from_orm(feedback)
    feedback_answer.answer_content = body.answer_content
    db.session.add(feedback_answer)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.error("error occupied during creation of feedback answer")

    return {"code": 0, "message": "ok"}, HTTPStatus.OK

