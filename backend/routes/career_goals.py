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
)


from schemas.career_goals import (
    CareerGoals as career_goals_schema,
    GoalCheckpoints as goal_checkpoint_schema,
)
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
    all_career_goals = db.session.execute(
        select(
            career_goals_schema
        )
        .limit(query.limit)
        .offset(query.skip)
    ).scalars().all()

    parsed = []

    for career_goal in all_career_goals:
        parsed_career_goal = career_goals_model.from_orm(career_goal)

        career_goal_id = parsed_career_goal.id

        all_goal_checkpoints = db.session.execute(
        select(
            goal_checkpoint_schema
        )
        .where(goal_checkpoint_schema.career_goal_id == career_goal_id)
        ).scalars().all()

        parsed_goal_checkpoints = []
        for goal_checkpoint in all_goal_checkpoints:
            parsed_goal_checkpoint = goal_checkpoint_model.from_orm(goal_checkpoint)
            parsed_goal_checkpoints.append(parsed_goal_checkpoint.dict())

        parsed_goal_with_checkpoints = CareerGoalsWithGoalCheckpoints(**parsed_career_goal.dict())
        parsed_goal_with_checkpoints.goal_checkpoints = parsed_goal_checkpoints

        parsed.append(parsed_goal_with_checkpoints.dict())

    return parsed


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
