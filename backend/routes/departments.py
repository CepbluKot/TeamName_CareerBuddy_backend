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
async def get_all_departments():
    all_departments = db.session.execute(select(departments_schema)).scalars().all()

    parsed_departments = []

    for department in all_departments:
        parsed = departments_model.from_orm(department)
        parsed_departments.append(parsed.dict())

    return parsed_departments
