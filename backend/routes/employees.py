from http import HTTPStatus
from pydantic import BaseModel
from flask import Response
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Employees as employee_model
from schemas.employees import Employees as employees_schema
from settings import db


api = APIBlueprint(
    '/employees',
    __name__,
    url_prefix='/employees',
    # abp_tags=[tag],
    # abp_security=security,
    # abp_responses={"401": Unauthorized},
    # disable openapi UI
    doc_ui=True
)
employees_tag = Tag(name='employees', description='employees api')


@api.post("/employee", tags=[employees_tag])
def add_employee(body: employee_model):
    employee_db_record = employees_schema(**body.dict())
    db.session.add(employee_db_record)
    db.session.commit()
    return {"code": 0, "message": "ok"}, HTTPStatus.OK
