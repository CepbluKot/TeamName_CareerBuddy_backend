from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees import Roles as roles_model, RolesResponseList

from schemas.employees import Roles as roles_schema

from sqlalchemy import select
from sqlalchemy.orm import aliased
from typing import List

from settings import db


api = APIBlueprint("/roles", __name__, url_prefix="/roles", doc_ui=True)
roles_tag = Tag(name="roles", description="roles api")


@api.get(
    "/all_roles",
    tags=[roles_tag],
    responses={HTTPStatus.OK: RolesResponseList},
)
async def get_all_roles():
    all_roles = db.session.execute(select(roles_schema)).scalars().all()

    parsed_roles = []

    for role in all_roles:
        parsed = roles_model.from_orm(role)
        parsed_roles.append(parsed.dict())

    return parsed_roles
