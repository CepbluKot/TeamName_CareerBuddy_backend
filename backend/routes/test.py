import logging
import schemas.feedback
import pandas as pd
from http import HTTPStatus
from pydantic import BaseModel
from flask import Response
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Employees as employee_model
from schemas.employees import Employees as employees_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from settings import db, security

from decorators.auth import role_required

from sqlalchemy import select
from schemas.employees import Roles


api = APIBlueprint(
    "/test",
    __name__,
    url_prefix="/test",
    # abp_tags=[tag],
    # abp_security=security,
    # abp_responses={"401": Unauthorized},
    # disable openapi UI
    doc_ui=True,
)
employees_tag = Tag(name="test", description="test api")


@api.get("/test", security=security)
@jwt_required()
@role_required(["Human Resources"])
def testing():
    # try:
    current_user = get_jwt_identity()
    return {"code": 0, "message": current_user}, HTTPStatus.OK

    # except Exception as e:
    #     return {"code": 1, "message": "not_ok", "err": str(e)}, HTTPStatus.BAD_REQUEST
