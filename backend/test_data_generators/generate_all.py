import logging
from settings import app, db
from test_data_generators.generate_departments import generate_departments
from test_data_generators.generate_roles import generate_roles
from test_data_generators.generate_employees import generate_employees
from test_data_generators.generate_goals import generate_goals
from test_data_generators.generate_feedback import generate_feedback

from sqlalchemy import select

from schemas.employees import Employees


def generate_test_data():
    with app.app_context():
        print('start generating')
        generate_departments()
        generate_roles()
        generate_employees()

        employees_ids = db.session.execute(select(Employees.id)).scalars().all()
        
        for id in employees_ids:
            generate_goals(employee_id=id)

        generate_feedback()
        print('stop generating')
