from settings import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


class EmployeesAuth(db.Model):
    __tablename__ = "employees_auth"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)

    employee_id = mapped_column(ForeignKey("employees.id"))
