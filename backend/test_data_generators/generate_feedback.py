import logging
import datetime
from faker import Faker
from jinja2 import Environment, FileSystemLoader, select_autoescape
from random import randint

from schemas.feedback import Feedback, FeedbackTemplates
from schemas.employees import Employees, Departments
from settings import db
from sqlalchemy import select


fake = Faker()


def generate_feedback_templates(creator_employee_id: int):
    tempalte_1_content = open('feedback_templates/template1.json').read()
    tempalte_2_content = open('feedback_templates/template2.json').read()

    template1 = FeedbackTemplates(name=fake.text(20), content=tempalte_1_content, created_by_employee_id=creator_employee_id)
    template2 = FeedbackTemplates(name=fake.text(20), content=tempalte_2_content, created_by_employee_id=creator_employee_id)

    db.session.add(template1)
    db.session.add(template2)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'error occupied during generating feedback: {e}')


def generate_feedback_answer(from_employee_id: int, to_employee_id, template_id: int):
    generate_feedback_templates(from_employee_id)
    
    current_date = datetime.datetime.now()
    future_date = current_date + datetime.timedelta(days=365)

    jinja_env = Environment(
        loader=FileSystemLoader("test_feedback_templates"), 
        autoescape=select_autoescape(['html', 'xml', 'json']) 
    )

    template = jinja_env.get_template(f'template{template_id}.json.j2')

    if template_id == 1:
        data = {
            "workload_answer": fake.text(max_nb_chars=123),  
            "work_life_balance_answer": randint(1,4),  
        }

    elif template_id == 2:
        data = {
            "workload_answer": fake.text(max_nb_chars=123),  
            "environment_satisfaction_answer": randint(1,4),  
            "job_involvement_answer": randint(1,4),  
            "job_level_answer": randint(1,5),  
            "job_satisfaction_answer": randint(1,4),  
            "performance_rating_answer": randint(1,4),  
            "relationship_satisfaction_answer": randint(1,4),  
            "work_life_balance_answer": randint(1,4),  
        }

    answer_body = template.render(**data)

    new_feedback = Feedback(from_employee_id=from_employee_id,
                            to_employee_id=to_employee_id,
                            template_id=template_id,
                            answer_content=answer_body,
                            date_sent=current_date,
                            date_answered=future_date)


    db.session.add(new_feedback)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'error occupied during generating feedback: {e}')


def generate_feedback():
    hr_employees = db.session.execute(select(Employees.id, Departments.name).filter(Employees.role_id == Departments.id).filter(Departments.name == "Human Resources")).all()
    not_hr_employees = db.session.execute(select(Employees.id, Departments.name).filter(Employees.role_id == Departments.id).filter(Departments.name != "Human Resources")).all()


    for hr_data in hr_employees:
        hr_id = hr_data[0]

        for not_hr_data in not_hr_employees:
            not_hr_id = not_hr_data[0]
            generate_feedback_answer(hr_id, not_hr_id, 1)
            generate_feedback_answer(hr_id, not_hr_id, 2)
