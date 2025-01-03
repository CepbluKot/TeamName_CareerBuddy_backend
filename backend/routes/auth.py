import logging
import random
import datetime
import faker
from http import HTTPStatus
from pydantic import BaseModel
from flask import Response, jsonify
from flask_openapi3 import Info, Tag
from flask_openapi3 import APIBlueprint, OpenAPI
from models.employees_auth import EmployeesAuth, EmployeesAuthRegister
from models.employees import Employees as employees_model
from schemas.employees_auth import EmployeesAuth as employees_auth_schema

from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from settings import db, token_live_time, security
from sqlalchemy import select
from schemas.employees import Roles, Departments, Employees as employees_schema

from flask_jwt_extended import create_access_token
from decorators.auth import role_required


api = APIBlueprint("/auth", __name__, url_prefix="/auth", doc_ui=True)
auth_tag = Tag(name="auth", description="auth api")
f = faker.Faker()


@api.post(
    "/register",
)
async def register(body: EmployeesAuthRegister):
    if body.id == 0:
        body.id = None


    is_login_exists = db.session.execute(
        select(employees_auth_schema.login).where(
            employees_auth_schema.login == body.login
        )
    ).scalar()
    if is_login_exists:
        return {
            "msg": "user with this login already registered",
        }, HTTPStatus.BAD_REQUEST

    # role_ids = list(db.session.execute(select(Roles.id)).scalars())
    department_ids = list(db.session.execute(select(Departments.id)).scalars())
    business_travels = list(
        db.session.execute(select(employees_schema.business_travel).distinct())
        .scalars()
        .all()
    )
    educations = list(
        db.session.execute(select(employees_schema.education).distinct())
        .scalars()
        .all()
    )
    education_fields = list(
        db.session.execute(select(employees_schema.education_field).distinct())
        .scalars()
        .all()
    )

    # if not role_ids:
    #     role_ids = [1]

    if not department_ids:
        department_ids = [1]

    if not business_travels:
        business_travels = ["Travel_Rarely"]

    if not educations:
        educations = [1]

    if not education_fields:
        education_fields = ["Other"]

    # last_employee_num = db.session.execute(
    #     select(employees_schema.employee_number).order_by(
    #         employees_schema.employee_number.desc()
    #     )
    # ).scalar()
    # if not last_employee_num:
    #     last_employee_num = 1

    age = random.randint(20, 100)
    total_working_years = random.randint(5, age)
    experience = total_working_years
    years_at_company = random.randint(1, experience)
    years_in_current_role = random.randint(1, years_at_company)
    years_since_last_promotion = random.randint(1, years_in_current_role)
    years_with_cur_manager = random.randint(1, years_in_current_role)

    employee_db_record = employees_schema(
        # id=last_employee_num,
        name=f.name()[0],
        surname=f.name()[1],
        email=f.email(),
        department_id=random.choice(department_ids),
        role_id=body.role_id,
        experience=experience,
        age=age,
        business_travel=random.choice(business_travels),
        daily_rate=random.randint(200, 1500),
        distance_from_home=random.randint(1, 100),
        education=random.choice(educations),
        education_field=random.choice(education_fields),
        relationship_satisfaction=random.randint(1, 4),
        standard_hours=80,
        stock_option_level=random.randint(0, 2),
        total_working_years=total_working_years,
        training_time_last_year=random.randint(1, 6),
        work_life_balance=random.randint(1, 4),
        years_at_company=years_at_company,
        years_in_current_role=years_in_current_role,
        years_since_last_promotion=years_since_last_promotion,
        years_with_cur_manager=years_with_cur_manager,
    )

    db.session.add(employee_db_record)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"error occupied during registering employee: {e}")
        return {"msg": "error"}, HTTPStatus.BAD_REQUEST

    db.session.refresh(employee_db_record)
    new_employee_id = employee_db_record.id

    print('new employee id', new_employee_id)

    employee_auth_db_schema = employees_auth_schema(
        login=body.login,
        password=body.password,
        is_active=True,
        employee_id=new_employee_id,
    )

    db.session.add(employee_auth_db_schema)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"error occupied during registering employee: {e}")
        return {"msg": "error"}, HTTPStatus.BAD_REQUEST
    
    return {"msg": "ok"}, HTTPStatus.OK


@api.post(
    "/login",
)
async def login(body: EmployeesAuth):
    id_in_db = db.session.execute(
        select(employees_auth_schema.employee_id).where(
            employees_auth_schema.login == body.login
        )).scalar()
    if not id_in_db:
        return {
            "msg": "user with this login not registered",
        }, HTTPStatus.BAD_REQUEST
    print('id in db', id_in_db)

    password_in_db = db.session.execute(
        select(employees_auth_schema.password)
        .where(employees_auth_schema.password == body.password)
        .where(employees_auth_schema.login == body.login)
    ).scalar()

    if not password_in_db:
        return { "msg": "wrong password"}, HTTPStatus.BAD_REQUEST

    
    role_id = db.session.execute(
        select(employees_schema.role_id)
        .where(employees_schema.id == id_in_db)
    ).scalar()

    role_name = db.session.execute(
        select(Roles.name)
        .where(Roles.id == role_id)
    ).scalar()

    identity = {"id": id_in_db, "role": role_name}

    access_token = create_access_token(identity=identity, expires_delta=token_live_time)
    return jsonify(access_token=access_token)


@api.post("/refresh_token", security=security)
@jwt_required()
async def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


@api.get("/me", security=security)
@jwt_required()
@role_required([])
async def testing():
    # try:
    current_user = get_jwt_identity()
    return { "msg": current_user}, HTTPStatus.OK
