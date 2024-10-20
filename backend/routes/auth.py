from http import HTTPStatus
from pydantic import BaseModel
from flask import Response
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees_auth import EmployeeAuthForm as employee_auth_model
from schemas.employees_auth import EmployeesAuth as employees_auth_schema

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt


api = APIBlueprint(
    '/auth',
    __name__,
    url_prefix='/auth',
    # abp_tags=[tag],
    # abp_security=security,
    # abp_responses={"401": Unauthorized},
    # disable openapi UI
    doc_ui=True
)
auth_tag = Tag(name='auth', description='auth api')


@api.post("/register", )
def register(body: employee_auth_model):

    return {"code": 0, "message": "ok"}, HTTPStatus.OK
