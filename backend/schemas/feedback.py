from settings import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    from_employee_id = mapped_column(ForeignKey("employees.id"))
    to_employee_id = mapped_column(ForeignKey("employees.id"))
    template_id = mapped_column(ForeignKey("feedback_templates.id"))
    answer_content = db.Column(db.String)
    date_sent = db.Column(db.DateTime)
    date_answered = db.Column(db.DateTime)


class FeedbackTemplates(db.Model):
    __tablename__ = "feedback_templates"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    content = db.Column(db.String)
    created_by_employee_id = mapped_column(ForeignKey("employees.id"))
