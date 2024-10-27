import logging
from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI

from models.career_goals import (
    CareerGoals as career_goals_model,
    GoalCheckpoints as goal_checkpoint_model,
    CareerGoalsWithGoalCheckpoints,
    CareerGoalsWithGoalCheckpointsList,
    GetAllFeedbackFilter,
    GetFilteredFeedbackFilter,
)


from schemas.career_goals import (
    CareerGoals as career_goals_schema,
    GoalCheckpoints as goal_checkpoint_schema,
)
from schemas.employees import Employees as employees_schema

from sqlalchemy import select
from sqlalchemy.orm import aliased
from typing import List

from settings import db


api = APIBlueprint("/career_goals", __name__, url_prefix="/career_goals", doc_ui=True)
career_goals_tag = Tag(name="career_goals", description="career goals api")


@api.get(
    "/all_career_goals",
    tags=[career_goals_tag],
    responses={HTTPStatus.OK: CareerGoalsWithGoalCheckpointsList},
)
def get_all_career_goals(query: GetAllFeedbackFilter):
    all_career_goals = (
        db.session.execute(
            select(career_goals_schema).limit(query.limit).offset(query.skip)
        )
        .scalars()
        .all()
    )

    parsed = []

    for career_goal in all_career_goals:
        parsed_career_goal = career_goals_model.from_orm(career_goal)

        career_goal_id = parsed_career_goal.id

        all_goal_checkpoints = (
            db.session.execute(
                select(goal_checkpoint_schema).where(
                    goal_checkpoint_schema.career_goal_id == career_goal_id
                )
            )
            .scalars()
            .all()
        )

        parsed_goal_checkpoints = []
        for goal_checkpoint in all_goal_checkpoints:
            parsed_goal_checkpoint = goal_checkpoint_model.from_orm(goal_checkpoint)
            parsed_goal_checkpoints.append(parsed_goal_checkpoint.dict())

        parsed_goal_with_checkpoints = CareerGoalsWithGoalCheckpoints(
            **parsed_career_goal.dict()
        )
        parsed_goal_with_checkpoints.goal_checkpoints = parsed_goal_checkpoints

        parsed.append(parsed_goal_with_checkpoints.dict())

    return parsed


@api.get(
    "/filtered_career_goals",
    tags=[career_goals_tag],
    responses={HTTPStatus.OK: CareerGoalsWithGoalCheckpointsList},
)
def get_filtered_career_goals(query: GetFilteredFeedbackFilter):
    employee_alias_for_department_id = aliased(employees_schema)
    employee_alias_for_role_id = aliased(employees_schema)

    filtered_career_goals = select(career_goals_schema)

    if query.employee_id != -1:
        filtered_career_goals = filtered_career_goals.filter(
            career_goals_schema.employee_id == query.employee_id
        )

    if query.department_id and query.department_id != -1:
        filtered_career_goals = filtered_career_goals.join(
            employee_alias_for_department_id,
            employee_alias_for_department_id.id == career_goals_schema.employee_id,
        ).filter(employee_alias_for_department_id.department_id == query.department_id)

    if query.role_id and query.role_id != -1:
        filtered_career_goals = filtered_career_goals.join(
            employee_alias_for_role_id,
            employee_alias_for_role_id.id == career_goals_schema.employee_id,
        ).filter(employee_alias_for_role_id.role_id == query.role_id)

    if query.skip and query.skip != -1:
        filtered_career_goals = filtered_career_goals.offset(query.skip)

    if query.limit and query.limit != -1:
        filtered_career_goals = filtered_career_goals.limit(query.limit)
    else:
        filtered_career_goals = filtered_career_goals.limit(100)

    all_career_goals = db.session.execute(filtered_career_goals).scalars().all()

    print("career goals filter res ", all_career_goals)

    parsed = []

    for career_goal in all_career_goals:
        parsed_career_goal = career_goals_model.from_orm(career_goal)

        career_goal_id = parsed_career_goal.id

        all_goal_checkpoints = (
            db.session.execute(
                select(goal_checkpoint_schema).where(
                    goal_checkpoint_schema.career_goal_id == career_goal_id
                )
            )
            .scalars()
            .all()
        )

        parsed_goal_checkpoints = []
        for goal_checkpoint in all_goal_checkpoints:
            parsed_goal_checkpoint = goal_checkpoint_model.from_orm(goal_checkpoint)
            parsed_goal_checkpoints.append(parsed_goal_checkpoint.dict())

        parsed_goal_with_checkpoints = CareerGoalsWithGoalCheckpoints(
            **parsed_career_goal.dict()
        )
        parsed_goal_with_checkpoints.goal_checkpoints = parsed_goal_checkpoints

        parsed.append(parsed_goal_with_checkpoints.dict())

    return parsed


@api.post("/create_career_goal", tags=[career_goals_tag])
def create_career_goal(body: career_goals_model):
    does_employee_exists = db.session.execute(select(employees_schema).filter(employees_schema.id == body.employee_id)).scalar()
    if not does_employee_exists:
        return {"code": 1, "message": "employee doesnt exist"}, HTTPStatus.OK

    
    career_goal_db_record = career_goals_schema(
        employee_id=body.employee_id,
        name=body.name,
        description=body.description,
        start_date=body.start_date,
        end_date=body.end_date,
    )

    db.session.add(career_goal_db_record)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.info("error occupied during creation of career goal")

    return {"code": 0, "message": "ok"}, HTTPStatus.OK



@api.post("/create_goal_checkpoint", tags=[career_goals_tag])
def create_goal_checkpoint(body: goal_checkpoint_model):
    does_career_goal_exists = db.session.execute(select(career_goals_schema).filter(career_goals_schema.id == body.career_goal_id)).scalar()
    if not does_career_goal_exists:
        return {"code": 1, "message": "career goals doesnt exist"}, HTTPStatus.OK


    goal_checkpoint_db_record = goal_checkpoint_schema(
        career_goal_id=body.career_goal_id,
        description=body.description,
        start_date=body.start_date,
        end_date=body.end_date,
    )

    db.session.add(goal_checkpoint_db_record)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logging.info("error occupied during creation of career goal")

    return {"code": 0, "message": "ok"}, HTTPStatus.OK
