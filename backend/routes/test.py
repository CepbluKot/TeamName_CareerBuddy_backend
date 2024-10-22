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
from settings import db

from sqlalchemy import select
from schemas.employees import Roles


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
    # try:
        df = pd.read_csv('dataset.csv')
        for index, row in df.iterrows():
            job_role =  row["JobRole"]
            role_data = db.session.execute(select(Roles.id).where(Roles.name == job_role)).scalars().first()
            break
        
        logging.info('role_data', job_role ,role_data)
        return {"code": 0, "message": "ok", "res": str(role_data), "job": str(job_role)}, HTTPStatus.OK

    # except Exception as e:
    #     return {"code": 1, "message": "not_ok", "err": str(e)}, HTTPStatus.BAD_REQUEST
