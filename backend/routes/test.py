from http import HTTPStatus
from pydantic import BaseModel
from flask import Response
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Employees as employee_model
from schemas.employees import Employees as employees_schema
import schemas.career_goals
import schemas.feedback
from settings import db
from uuid import UUID, uuid4


api = APIBlueprint(
    '/test',
    __name__,
    url_prefix='/test',
    # abp_tags=[tag],
    # abp_security=security,
    # abp_responses={"401": Unauthorized},
    # disable openapi UI
    doc_ui=True
)
employees_tag = Tag(name='test', description='test api')


@api.get("/test", )
def testing():
    return {"code": 0, "message": "ok"}, HTTPStatus.OK
