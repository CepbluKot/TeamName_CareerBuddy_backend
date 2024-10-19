from settings import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
import uuid


class Employees(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    department = db.Column(db.String)
    role_id = db.Column(db.Integer)
    experience = db.Column(db.Float)
    age = db.Column(db.Integer)
    business_travel = db.Column(ARRAY(db.String))
    daily_rate = db.Column(db.Integer)
    distance_from_home = db.Column(db.Integer)
    education = db.Column(db.Integer)
    education_field = db.Column(ARRAY(db.String))
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
