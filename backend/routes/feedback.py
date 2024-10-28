import logging
from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.feedback import GetFilteredFeedback

from models.feedback import (
    Feedback as feedback_model,
    FeedbackList,
    GetAllFeedback,
    CreateFeedback,
    CreateFeedbackAnswer,
    FeedbackTemplateList,
    FeedbackTemplate as feedback_template_model,
    GetUsersFeedbackTemplate,
)

from schemas.feedback import (
    Feedback as feedback_schema,
    FeedbackTemplates as feedback_template_schema,
)
from schemas.employees import (
    Employees as employees_schema,
    Departments as departments_schema,
    Roles as roles_schema,
)
from sqlalchemy import select, update
from sqlalchemy.orm import aliased
from typing import List

from settings import db, security
from services.employees import get_filtered_employees as get_filtered_employees_func
from datetime import datetime

from decorators.auth import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity


api = APIBlueprint("/feedback", __name__, url_prefix="/feedback", doc_ui=True)
feedback_tag = Tag(name="feedback", description="employees api")


@api.get(
    "/filtered_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList}, 
    security=security
)
@jwt_required()
@role_required(["Human Resources"])
async def get_filtered_feedback(query: GetFilteredFeedback):
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

    parsed_feedback = []

    for feedback in all_feedback:
        parsed = feedback_model.from_orm(feedback)
        parsed_feedback.append(parsed.dict())

    return parsed_feedback




@api.get(
    "/my_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList}, 
    security=security
)
@jwt_required()
@role_required([])
async def my_filtered_feedback(query: GetAllFeedback):
    current_user = get_jwt_identity()
    current_user_id = current_user.get("id")

    filtered_feedback_query = select(feedback_schema)

    employee_alias_for_department_id = aliased(employees_schema)
    employee_alias_for_role_id = aliased(employees_schema)

    filtered_feedback_query = filtered_feedback_query.filter(
        feedback_schema.to_employee_id == current_user_id
    )

    if query.limit and query.limit != -1:
        filtered_feedback_query = filtered_feedback_query.limit(query.limit)

    else:
        filtered_feedback_query = filtered_feedback_query.limit(100)

    if query.skip and query.skip != -1:
        filtered_feedback_query = filtered_feedback_query.offset(query.skip)

    all_feedback = db.session.execute(filtered_feedback_query).scalars().all()

    parsed_feedback = []

    for feedback in all_feedback:
        parsed = feedback_model.from_orm(feedback)
        parsed_feedback.append(parsed.dict())

    return parsed_feedback


@api.get(
    "/all_feedback",
    tags=[feedback_tag],
    responses={HTTPStatus.OK: FeedbackList}, 
    security=security
)
@jwt_required()
@role_required(["Human Resources"])
async def get_all_feedback(query: GetAllFeedback):
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
    security=security
)
@jwt_required()
@role_required(["Human Resources"])
async def get_all_feedback_templates(query: GetAllFeedback):
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
    security=security
)
@jwt_required()
@role_required(["Human Resources"])
async def get_users_feedback_template(query: GetUsersFeedbackTemplate):
    all_feedback = (
        db.session.execute(
            select(feedback_template_schema)
            .limit(query.limit)
            .offset(query.skip)
            .where(feedback_template_schema.created_by_employee_id == 1)
        )
        .scalars()
        .all()
    )

    parsed_feedback_templates = []

    for feedback in all_feedback:
        parsed = feedback_template_model.from_orm(feedback)
        parsed_feedback_templates.append(parsed.dict())

    return parsed_feedback_templates


@api.post("/create_feedback_template", tags=[feedback_tag], 
    security=security)
@jwt_required()
@role_required(["Human Resources"])
async def create_feedback_template(body: feedback_template_model):
    current_user = get_jwt_identity()
    current_user_id = current_user.get("id")

    new_feedback_template = feedback_template_schema(
        name=body.name, content=body.content, created_by_employee_id=current_user_id
    )
    db.session.add(new_feedback_template)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.error("error occupied during creation of new feedback template")
        return {"msg": "error"}, HTTPStatus.BAD_REQUEST
        return {"msg": "error"}, HTTPStatus.BAD_REQUEST
    
    return {"msg": "ok"}, HTTPStatus.OK


@api.post(
    "/create_feedback",
    tags=[feedback_tag], 
    security=security
)
@jwt_required()
@role_required(["Human Resources"])
async def create_feedback(body: CreateFeedback):
    current_user = get_jwt_identity()
    current_user_id = current_user.get("id")

    does_template_exists = db.session.execute(
        select(feedback_template_schema).where(
            feedback_template_schema.id == body.feedback_form_template_id
        )
    ).scalar()

    if not does_template_exists:
        return {
            "msg": "feedback template doesnt exist",
        }, HTTPStatus.BAD_REQUEST

    if body.to_employee_id == -1:
        filtered_employees = get_filtered_employees_func(
            department_id=body.department_id, role_id=body.role_id
        )

    else:
        filtered_employees = [{"id": body.to_employee_id}]

    for employee in filtered_employees:
        print('sending to id', employee.get('id'))
        new_feedback = feedback_schema(
            from_employee_id=current_user_id,
            to_employee_id=employee.get('id'),
            date_sent=datetime.now(),
            template_id=body.feedback_form_template_id,
        )
        db.session.add(new_feedback)

        print('sending this', new_feedback)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.error("error occupied during creation of new feedback")
        return {"msg": "error"}, HTTPStatus.BAD_REQUEST
    
    return {"msg": "ok"}, HTTPStatus.OK


@api.post(
    "/create_feedback_answer",
    tags=[feedback_tag], 
    security=security
)
@jwt_required()
@role_required([])
async def create_feedback_answer(body: CreateFeedbackAnswer):
    current_user = get_jwt_identity()
    current_user_id = current_user.get("id")


    db.session.execute(
        update(feedback_schema).where(feedback_schema.id == body.feedback_id).values(answer_content=body.answer_content, date_answered=datetime.now())
    )
    db.session.commit()

    # try:
    #     db.session.commit()
    # except Exception:
    #     db.session.rollback()
    #     logging.error("error occupied during creation of feedback answer")
    #     return {"msg": "error"}, HTTPStatus.BAD_REQUEST

    return { "msg": "ok"}, HTTPStatus.OK
