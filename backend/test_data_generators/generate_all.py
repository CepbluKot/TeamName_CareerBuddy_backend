from settings import app
from test_data_generators.generate_departments import generate_departments
from test_data_generators.generate_roles import generate_roles
from test_data_generators.generate_employees import generate_employees


def generate_test_data():
    with app.app_context():
        generate_departments()
        generate_roles()
        generate_employees()
