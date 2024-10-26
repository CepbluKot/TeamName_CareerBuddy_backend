from settings import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


class CareerGoals(db.Model):
    __tablename__ = 'career_goals'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = mapped_column(ForeignKey("employees.id"))
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)


class GoalCheckpoints(db.Model):
    __tablename__ = 'goal_checkpoints'
    id = db.Column(db.Integer, primary_key=True)
    career_goal_id = mapped_column(ForeignKey("career_goals.id"))
    description = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
