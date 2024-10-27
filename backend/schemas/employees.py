from settings import db
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy.dialects.postgresql import ARRAY


class Employees(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=None)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    department_id = mapped_column(db.Integer, ForeignKey("departments.id"))
    role_id = mapped_column(db.Integer, ForeignKey("roles.id"))
    experience = db.Column(db.Float)
    age = db.Column(db.Integer)
    business_travel = db.Column(db.String)
    daily_rate = db.Column(db.Integer)
    distance_from_home = db.Column(db.Integer)
    education = db.Column(db.Integer)
    education_field = db.Column(db.String)
    employee_number = db.Column(db.Integer)
    relationship_satisfaction = db.Column(db.Integer)
    standard_hours = db.Column(db.Integer)
    stock_option_level = db.Column(db.Integer)
    total_working_years = db.Column(db.Integer)
    training_time_last_year = db.Column(db.Integer)
    work_life_balance = db.Column(db.Integer)
    years_at_company = db.Column(db.Integer)
    years_in_current_role = db.Column(db.Integer)
    years_since_last_promotion = db.Column(db.Integer)
    years_with_cur_manager = db.Column(db.Integer)


class Roles(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    admin_page = db.Column(db.Boolean)
    feedback_page = db.Column(db.Boolean)
    career_goal_page = db.Column(db.Boolean)


class Departments(db.Model):
    __tablename__ = "departments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
